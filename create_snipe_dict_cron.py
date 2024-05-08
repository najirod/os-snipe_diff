import snipeitpyapi as snipeit
from snipeitpyapi import Assets
import requests
import json
from importlib import reload
from dotenv import load_dotenv
import os
from openpyxl import load_workbook
from openpyxl import Workbook
from datetime import date
from deepdiff import DeepDiff
import diff
import ExcelReport
import sys
import logging
###############################
reload(snipeit)

if "venv" in sys.path[0]:
    root_path = (sys.path[1] + "/")
else:
    root_path = (sys.path[0] + "/")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(pathname)s:%(funcName)s:%(name)s:%(process)d:%(message)s')

file_handler = logging.FileHandler(root_path + 'logs/cron_py.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



class Snipe:
    def __init__(self):

        # root_path = (sys.path[1] + "/")  # /Users/dpustahija1/PycharmProjects/os-snipe_diff/
        dotenv_path = (root_path + ".env")
        # print(dotenv_path)
        load_dotenv(dotenv_path=dotenv_path)
        self.all_assets = snipeit.Assets()
        self.server = os.getenv("server")  # snipe-it server IP
        self.token = os.getenv("token")  # personal token for snipe API
        self.limit1 = os.getenv("limit1")  # limit for snipe API GET {int} -- None = All
        self.offset1 = os.getenv("offset1")  # offset {int} -- default: {0}
        self.limit2 = os.getenv("limit2")  # limit for snipe API GET {int} -- None = All
        self.offset2 = os.getenv("offset2")  # offset {int} -- default: {0}
        self.total = ""  # number of items assets in snipe {str}

        self.asset_tags = []  # list of all asset tags in snipe-it in order
        self.serial = []  # list of all serial/IMEI in snipe-it in order
        self.supplier = []  # list of suppliers for assets in order
        self.os_number = []  # list of os numbers for assets in order
        self.person = []  # list of people names or usernames for assets in order - if Ready to Deploy then "rtd"
        self.asset_name = []  # list of asset names from snipe-it in order
        self.last_audit_date = []  # list of last audit dates
        self.next_audit_date = []  # list of next audit dates

        self.merged_data = []

        self.export_raw_results_path = (root_path + os.getenv("export_raw_results_path_cron"))
        self.export_pretty_results_path = (root_path + os.getenv("export_pretty_results_path_cron"))
        self.dict_from_snipe_data = {}  # dict wih needed data from snipe-it

        headers = {"Accept": "application/json", "Authorization": ("Bearer " + self.token)}
        response = requests.get(self.server+"/api/v1/hardware", headers=headers)
        # print(response)
        logger.info(response)


    # append list of all assets from snipe to "merged_data"(!!! MAX - 4500 !!!)
    def get_merged_raw_data_from_snipe(self):
        logger.info("Starting to fetch data from snipeit")
        raw_data_from_snipe = self.all_assets.get(server=self.server, token=self.token, limit=self.limit1,
                                                  offset=self.offset1)
        raw_data_from_snipe_2 = self.all_assets.get(server=self.server, token=self.token, limit=self.limit2,
                                                    offset=self.offset2)
        raw_data_from_snipe_3 = self.all_assets.get(server=self.server, token=self.token, limit=self.limit3,
                                                    offset=self.offset3)
        json_object_snipe = json.loads(raw_data_from_snipe)
        json_object_snipe_2 = json.loads(raw_data_from_snipe_2)
        json_object_snipe_3 = json.loads(raw_data_from_snipe_3)

        self.total = json_object_snipe["total"]
        l1_l2_l3 = (json_object_snipe['rows'] + json_object_snipe_2['rows'] + json_object_snipe_3['rows'])
        with open(self.export_raw_results_path + '.raw_data.json', 'w') as outfile:
            json.dump(l1_l2_l3, outfile)
        with open(self.export_raw_results_path + 'raw_data ' + date.today().strftime("%d.%m.%Y") + '.json',
                  'w') as outfile:
            json.dump(l1_l2_l3, outfile)
        with open(self.export_raw_results_path + '.raw_data.json') as j_full:
            self.merged_data = json.load(j_full)
        # return merged_data
        logger.info("Fetched raw data")

    # appends list of all: asset_tags, serials, suppliers, os_numbers - if None = None
    def get_all_data_from_snipe(self):
        logger.info("Starting to process data")
        for i in range(int(self.total)):
            self.asset_tags.append(self.merged_data[i]['asset_tag'])
            self.serial.append(self.merged_data[i]['serial'])

            if self.merged_data[i]['supplier'] is None:
                self.supplier.append(None)
            else:
                self.supplier.append(self.merged_data[i]['supplier']['name'])
            if list(self.merged_data[i]['custom_fields'].keys())[0] == 'ZOPU':
                if self.merged_data[i]['custom_fields']['Broj osnovnog sredstva']['value'] is None:
                    self.os_number.append(None)
                else:
                    self.os_number.append(self.merged_data[i]['custom_fields']['Broj osnovnog sredstva']['value'])
            elif list(self.merged_data[i]['custom_fields'].keys())[0] == 'Broj kartice':
                # print("kartica")
                self.os_number.append(None)
            if self.merged_data[i]["assigned_to"] is None:
                self.person.append("rtd")
            else:
                if self.merged_data[i]["assigned_to"]["name"] is None:
                    self.person.append(self.merged_data[i]["assigned_to"]["username"])
                else:
                    self.person.append(self.merged_data[i]["assigned_to"]["name"])

            if self.merged_data[i]['model']['name'] is None:
                self.asset_name.append("no name")

            else:
                self.asset_name.append(self.merged_data[i]["model"]["name"])

            if self.merged_data[i]['last_audit_date'] is None:
                self.last_audit_date.append(None)
            else:
                self.last_audit_date.append(self.merged_data[i]['last_audit_date']["formatted"])

            if self.merged_data[i]['next_audit_date'] is None:
                self.next_audit_date.append(None)
            else:
                self.next_audit_date.append(self.merged_data[i]['next_audit_date']['formatted'])
        logger.info("Data processing is done")
    # creates dict of needed data from snipe
    def create_dict_from_snipe_data(self):
        logger.info("Starting to create pretty Json")
        keys_for_l2_dict = ["person", "asset_name", "serial", "supplier", "os_number", "last_audit_date", "next_audit_date"]
        self.dict_from_snipe_data = dict.fromkeys(self.asset_tags)
        for key in self.dict_from_snipe_data:
            key_index = self.asset_tags.index(key)
            self.dict_from_snipe_data[key] = dict.fromkeys(keys_for_l2_dict)
            self.dict_from_snipe_data[key]["person"] = self.person[key_index]
            self.dict_from_snipe_data[key]["asset_name"] = self.asset_name[key_index]
            self.dict_from_snipe_data[key]["serial"] = self.serial[key_index]
            self.dict_from_snipe_data[key]["supplier"] = self.supplier[key_index]
            self.dict_from_snipe_data[key]["os_number"] = self.os_number[key_index]
            self.dict_from_snipe_data[key]["last_audit_date"] = self.last_audit_date[key_index]
            self.dict_from_snipe_data[key]["next_audit_date"] = self.next_audit_date[key_index]
        with open(self.export_pretty_results_path + 'dict_from_snipe_data_' + date.today().strftime("%d.%m.%Y") + '.json', 'w') as write_file:
            json.dump(self.dict_from_snipe_data, write_file)
        logger.info("Created pretty Json :)")


    def get(self):
        self.get_merged_raw_data_from_snipe()
        self.get_all_data_from_snipe()
        self.create_dict_from_snipe_data()

if __name__ == "__main__":
    snipe = Snipe()
    snipe.get()