
import binascii
import hashlib
import os
import secrets
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import google_api
from framework_utils import config
from mailgun import Mailgun
from receipt_statments import PdfStatement

root_path = config.get_root_path()
logger = config.configure_logging(log_file_name="log_freeradius.log", logger_name=__name__)


class Freeradius:
    def __init__(self):
        dotenv_path = (root_path + ".env")
        load_dotenv(dotenv_path=dotenv_path)

        radius_db_name = os.getenv("radius_db_name")
        radius_db_user = os.getenv("radius_db_user")
        radius_db_password = os.getenv("radius_db_password")
        radius_db_ipaddress = os.getenv("radius_db_ipaddress")

        # Establish a connection to the Radius database
        engine_radius = create_engine(f"mysql+mysqlconnector://{radius_db_user}:{radius_db_password}@{radius_db_ipaddress}/{radius_db_name}")
        self.radius_session = Session(engine_radius)
        Base = automap_base()
        Base.prepare(autoload_with=engine_radius)
        self.Radcheck = Base.classes.radcheck
        self.Radusergroup = Base.classes.radusergroup

        # Initialize the Google Directory API
        self.g_api = google_api.GoogleDirectoryAPI('credentials.json',
                                                   'token.json')

    def ___generate_password(self, password=None, nbytes=6):
        """
        Generate a password hash using the NTLM algorithm.

        Args:
            password (str, optional): The password to hash. If not provided, a random password is generated.
            nbytes (int, optional): Number of bytes for generating a random password.

        Returns:
            str: The hexadecimal representation of the NTLM hash.
            str: The password used for hashing.
        """
        if not password:
            # Generate a random password if one is not provided
            password = secrets.token_urlsafe(nbytes=nbytes)

        # Encode the password as UTF-16LE (Little Endian) before hashing
        password_encoded = password.encode('utf-16le')

        # Create an MD4 hash object and compute the hash
        md4_hash = hashlib.new('md4', password_encoded).digest()

        # Convert the MD4 hash to a hexadecimal representation
        ntlm_hash = binascii.hexlify(md4_hash).decode('utf-8')

        return ntlm_hash, password

    def create_radius_user(self, username, password=None, notify=False, attribute="NT-Password", op=":=", groupname=None):
        """
        Create a new Radius user in the database.

        Args:
            username (str): The username for the new user.
            password (str, optional): The password for the new user. If not provided, a random password is generated.
            notify (bool, optional): Whether to notify user with email (default is False).
            attribute (str, optional): The attribute for the user (default is "NT-Password").
            op (str, optional): The operation (default is ":=").
            groupname (str, optional): The group name for the user (default is "Manual").

        Returns:
            str: A message indicating the result of the user creation.
        """
        try:
            # Check if the username already exists in the database
            existing_user = self.radius_session.query(self.Radcheck).filter_by(username=username).first()

            if existing_user:
                logger.warning(f"Username {username} already exists")
                return f"Username {username} already exists"

            if password is None:
                password, clear = self.___generate_password()

            else:
                password, clear = self.___generate_password(password=password)

            new_user = self.Radcheck(username=username, attribute=attribute, op=op, value=password)

            if groupname is None:
                groupname = "Manual"

            user_to_group = self.Radusergroup(username=username, groupname=groupname, priority=11)
            self.radius_session.add(new_user)
            self.radius_session.add(user_to_group)
            self.radius_session.commit()
            self.radius_session.close()

            if notify:
                self.send_credentials_email(email=username, clear_pass=clear)

            logger.info(f"User {username} created successfully")
            logger.info(f"User {username} added to group {groupname} successfully")
            return "User created successfully"
        except Exception as e:
            logger.critical(f"Error creating user {username}: {str(e)}")
            return "Error creating user"

    def create_radius_users_from_usernames_list(self, list_of_usernames=None, from_google=False, groupname=None):
        """
        Create Radius users from a list of usernames.

        Args:
            list_of_usernames (list, optional): List of usernames to create Radius users from.
            from_google (bool, optional): Whether to fetch usernames from Google (default is False).
            groupname (str, optional): The group name for the users (default is "Manual").

        Returns:
            str: A message indicating the result of the user creation.
        """
        if list_of_usernames is None and not from_google:
            return "User list is None"

        if from_google:
            list_of_usernames = self.g_api.get_users_by_location("SofaIT")
            groupname = "GoogleAuto"

        if groupname is None:
            groupname = "Manual"

        for user in list_of_usernames:
            self.create_radius_user(username=user, groupname=groupname)

    def deactivate_radius_user(self, username):
        """
        Deactivate a Radius user by adding them to the "Reject-group."

        Args:
            username (str): The username to deactivate.

        Returns:
            str: A message indicating the result of the user deactivation.
        """
        try:
            # Check if the username exists in the database
            existing_user = self.radius_session.query(self.Radcheck).filter_by(username=username).first()
            existing_users_in_group = self.radius_session.query(self.Radusergroup).filter_by(username=username).all()

            if not existing_user:
                logger.warning(f"Username {username} does not exist")
                return f"Username {username} does not exist"

            # Check if the user is already in the "Reject-group"
            is_already_deactivated = any(group.groupname == "Reject-group" for group in existing_users_in_group)

            if is_already_deactivated:
                logger.warning(f"User {username} is already in 'Reject-group'")
                return f"User {username} is already deactivated"

            # Add the user to the "Reject-group" with a high priority to reject authentication
            user_to_group = self.Radusergroup(username=username, groupname="Reject-group", priority=11)
            self.radius_session.add(user_to_group)
            self.radius_session.commit()
            self.radius_session.close()

            logger.info(f"User {username} deactivated successfully by adding to 'Reject-group'")
            return f"User {username} deactivated successfully"
        except Exception as e:
            logger.critical(f"Error deactivating user {username}: {str(e)}")
            return "Error deactivating user"

    def delete_radius_user(self, username):
        """
        Delete a Radius user from the database.

        Args:
            username (str): The username to delete.

        Returns:
            str: A message indicating the result of the user deletion.
        """
        try:
            # Check if the username exists in the database
            existing_user = self.radius_session.query(self.Radcheck).filter_by(username=username).first()
            existing_user_in_groups = self.radius_session.query(self.Radusergroup).filter_by(username=username).all()

            if not existing_user:
                logger.warning(f"Username {username} does not exist")
                return f"Username {username} does not exist"

            for group in existing_user_in_groups:
                self.radius_session.delete(group)

            self.radius_session.delete(existing_user)
            self.radius_session.commit()
            self.radius_session.close()

            logger.info(f"User {username} deleted successfully")
            logger.info(f"User {username} deleted from all groups successfully")
            return "User deleted successfully"
        except Exception as e:
            logger.critical(f"Error deleting user {username}: {str(e)}")
            return "Error deleting user"

    # TODO:
    def send_credentials_email(self, email, clear_pass):
        """
        Send a Radius email.

        Args:
            email (str): The email address to send to.
            clear_pass (str): The clear text password.

        Returns:
            None
        """
        wifi_credentials_statement = PdfStatement().wifi_credentials(username=email, password=clear_pass)

        mymailgun = Mailgun(sender=("Sender Ime", "Senderusername"))
        mymailgun.send_mail(recipient_email="dpustahija@gmail.com", subject="naslov", message="messagicahtml", attachment_bytes=wifi_credentials_statement)


if __name__ == "__main__":

    my_radius = Freeradius()
    # my_radius.delete_radius_user(username="dpustahija@gmail.com")
    # my_radius.create_radius_user(username="dpustahija@gmail.com", password="konj", notify=True)
    # my_radius.create_radius_users_from_usernames_list(list_of_usernames=["marko", "pero"])
    my_radius.create_radius_users_from_usernames_list(from_google=True)
    # my_radius.delete_radius_user(username="dpustahija@gmail.com")
    # my_radius.deactivate_radius_user(username="marko")
