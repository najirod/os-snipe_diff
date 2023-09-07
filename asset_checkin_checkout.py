import snipeitpyapi as snipeit
import json
from dotenv import load_dotenv
import os
import sys
from datetime import date
import logging
import requests

if "venv" in sys.path[0]:
    root_path = (sys.path[1] + "/")
else:
    root_path = (sys.path[0] + "/")

today_date = date.today().strftime("%d.%m.%Y")
#items = [{'item': "fdscdtfd"},{'item': "fdscdtfd"},{'item': "fdscdtfd"},]

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(pathname)s:%(funcName)s:%(name)s:%(process)d:%(message)s')

file_handler = logging.FileHandler(root_path + 'logs/log_py.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class AssetHandler:
    def __init__(self, list_of_asset_ids=None, list_of_asset_tags=None, user_id=None):
        dotenv_path = (root_path + ".env")
        load_dotenv(dotenv_path=dotenv_path)
        self.server = os.getenv("server")  # snipe-it server IP
        self.token = os.getenv("token")  # personal token for snipe API
        self.headers = {"accept": "application/json", "Authorization": "Bearer " + os.getenv("token"), "content-type": "application/json"}
        self.list_of_asset_ids = list_of_asset_ids
        self.list_of_asset_tags = list_of_asset_tags
        self.user_id = user_id
        self.asset = snipeit.Assets()

    def test_connection(self):

        url = f"{self.server}/api/v1/hardware/bytag/02721?deleted=false"


        response = requests.get(url, headers=self.headers)

        print(response.text)

    def id_from_asset_tag(self, asset_tag):
        if len(asset_tag) == 4:
            asset_tag = f"0{asset_tag}"
        json_object_details_from_tag = json.loads(
            self.asset.getDetailsByTag(server=self.server, token=self.token, AssetTag=asset_tag))
        id_from_tag = str(json_object_details_from_tag["id"])
        return str(id_from_tag)

    def check_in(self, asset_id):
        checkin_url = f"{self.server}/api/v1/hardware/{asset_id}/checkin"
        payload = {"status_id": 2}
        response = requests.post(checkin_url, json=payload, headers=self.headers)
        logger.info(response.text)

    def check_out(self, asset_id, user_id):
        checkout_url = f"{self.server}/api/v1/hardware/{asset_id}/checkout"
        payload = {
            "checkout_to_type": "user",
            "status_id": 2,
            "assigned_user": user_id
        }
        response = requests.post(checkout_url, json=payload, headers=self.headers)
        logger.info(response.text)

    def recheckout(self, asset_id, user_id):
        self.check_in(asset_id)
        self.check_out(asset_id, user_id=user_id)

    def bulk_checkin(self):
        if self.list_of_asset_ids is not None:
            for asset_id in self.list_of_asset_ids:
                self.check_in(asset_id=asset_id)
        elif self.list_of_asset_tags is not None:
            for asset_tag in self.list_of_asset_tags:
                self.check_in(asset_id=self.id_from_asset_tag(asset_tag=asset_tag))

    def bulk_checkout(self):
        if self.list_of_asset_ids is not None:
            for asset_id in self.list_of_asset_ids:
                self.check_out(asset_id=asset_id, user_id=self.user_id)
        elif self.list_of_asset_tags is not None:
            for asset_tag in self.list_of_asset_tags:
                self.check_out(asset_id=self.id_from_asset_tag(asset_tag=asset_tag), user_id=self.user_id)

    def bulk_recheckout(self):
        if self.list_of_asset_ids is not None:
            for asset_id in self.list_of_asset_ids:
                self.recheckout(asset_id=asset_id, user_id=self.user_id)
        elif self.list_of_asset_tags is not None:
            for asset_tag in self.list_of_asset_tags:
                self.recheckout(asset_id=self.id_from_asset_tag(asset_tag), user_id=self.user_id)


test_list = []
test_list_tags = ["02721"]
myasset = AssetHandler(list_of_asset_tags=test_list_tags, user_id="155")
# myasset.bulk_checkin()
#myasset.bulk_recheckout()
myasset.test_connection()
