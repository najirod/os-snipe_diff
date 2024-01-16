import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from framework_utils import config

root_path = config.get_root_path()
logger = config.configure_logging(log_file_name="log_google_api.log", logger_name=__name__)


class GoogleDirectoryAPI:
    def __init__(self, client_secrets_file, token_file):
        """
        Initialize the GoogleDirectoryAPI class.

        Args:
            client_secrets_file (str): The path to the client secrets JSON file.
            token_file (str): The path to the token JSON file.
        """
        dotenv_path = (root_path + ".env")
        load_dotenv(dotenv_path=dotenv_path)
        credentials_path = os.getenv("credentials_path")

        self.SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']
        self.client_secrets_file = f"{root_path}{credentials_path}/{client_secrets_file}"
        self.token_file = f"{root_path}{credentials_path}/{token_file}"
        self.creds = self.___get_credentials()

    def ___get_credentials(self):
        """
        Retrieve and manage Google API credentials.

        Returns:
            Credentials: The Google API credentials.
        """
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        return creds

    def get_raw_user_data(self):
        """
        Retrieve raw user data from the Google Admin Directory API.

        Returns:
            list: A list of raw user data.
        """
        service = build('admin', 'directory_v1', credentials=self.creds)

        user_data_list = []
        users = service.users().list(customer='my_customer', maxResults=500).execute()
        user_data_list.extend(users.get('users', []))

        while 'nextPageToken' in users:
            nextPageToken = users['nextPageToken']
            users = service.users().list(customer='my_customer', maxResults=1000, pageToken=nextPageToken).execute()
            user_data_list.extend(users.get('users', []))

        logger.info("Retrieved raw user data.")
        return user_data_list

    def get_user_data(self):
        """
        Process and format the raw user data into a more readable format.

        Returns:
            list: A list of formatted user data.
        """
        raw_data = self.get_raw_user_data()

        selected_user_data = []

        for user in raw_data:
            pretty_data = {
                "id": user.get("id", ""),
                "name": user.get("name", ""),
                "email": user.get("primaryEmail", ""),
                "locations": user.get("locations", [])
            }
            selected_user_data.append(pretty_data)

        logger.info("Processed and formatted user data.")
        return selected_user_data

    def get_users_by_location(self, location):
        """
        Retrieve user emails based on a specified location (e.g., "SofaIT").

        Args:
            location (str): The location to filter users by.

        Returns:
            list: A list of user emails in the specified location.
        """
        user_data = self.get_user_data()
        user_emails_in_location = []
        for user in user_data:
            # Check if "locations" key exists and contains dictionaries
            if "locations" in user and isinstance(user["locations"], list):
                # Loop through the "locations" list
                for user_location in user["locations"]:
                    # Check if "buildingId" is equal to the specified location
                    if "buildingId" in user_location and user_location["buildingId"] == location:
                        # Add the email to the filtered_emails list
                        user_emails_in_location.append(user["email"])

        logger.info(f"Retrieved user emails in location: {location}")
        return user_emails_in_location


if __name__ == '__main__':
    api = GoogleDirectoryAPI('credentials.json', 'token.json')
    # Example usage of the API functions
    # print(api.get_user_data())
    print(api.get_users_by_location("SofaIT"))
