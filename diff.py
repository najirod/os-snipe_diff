from deepdiff import DeepDiff
import json
import os
import re
import sys
from ExcelReport import Report
from dotenv import load_dotenv
import logging

from framework_utils import config

root_path = config.get_root_path()
logger = config.configure_logging("log_py.log", logger_name=__name__)


class Diff:
    def __init__(self, filename1, filename2, save_path=None, save_name="file"):
        # root_path = (sys.path[0] + "/") #/Users/dpustahija1/PycharmProjects/os-snipe_diff/
        dotenv_path = (root_path + ".env")
        #print(dotenv_path)
        load_dotenv(dotenv_path=dotenv_path)
        self.file1 = filename1
        self.file2 = filename2
        self.filename = save_name

        self.save_path = save_path
        self.path = (root_path + (os.getenv("diff_path")))
        # print("2",self.path)
        self.export_results_path_diff = (root_path + (os.getenv("export_results_path_diff")))

        self.differences = {}
        self.num_of_changes = 0
        self.num_of_added = 0
        self.num_of_removed = 0

        self.removed_tag = []

        self.added_tag = []

        self.changed_field = []

        self.asset_tag_person = []
        self.new_value_person = []
        self.old_value_person = []

        self.asset_tag_os_num = []
        self.new_value_os_num = []
        self.old_value_os_num = []

        self.asset_tag_misc = []
        self.new_value_misc = []
        self.old_value_misc = []

    def check_if_changed(self):
        with open(self.path + self.file1 + ".json", "r", encoding="utf-8") as json1:
            js1 = json.load(json1)
        with open(self.path + self.file2 + ".json", "r", encoding="utf-8") as json2:
            js2 = json.load(json2)

        self.differences = dict(DeepDiff(js1, js2))
        # print(self.differences)
        if self.differences == {}:
            #print("diff, check_if_changed", "0")
            logger.info("no changes")
            return "0"

    def get_diff(self):
        with open(self.path + self.file1 + ".json", "r", encoding="utf-8") as json1:
            js1 = json.load(json1)
        with open(self.path + self.file2 + ".json", "r", encoding="utf-8") as json2:
            js2 = json.load(json2)

        self.differences = dict(DeepDiff(js1, js2))

        if self.differences != {}:
            # print(self.differences.keys())
            if "values_changed" in self.differences.keys():
                self.num_of_changes = len(self.differences["values_changed"])
            if "dictionary_item_added" in self.differences.keys():
                self.num_of_added = len(self.differences["dictionary_item_added"])
            if "dictionary_item_removed" in self.differences.keys():
                self.num_of_removed = len(self.differences["dictionary_item_removed"])
        else:
            pass


    def create_json(self):
        if self.check_if_changed() == None:
            self.get_diff()
            logger.info("Start to create Json Report")
            with open(self.export_results_path_diff + 'diffs.json', 'w') as write_file:
                json.dump(self.differences, write_file)
            logger.info("Ended creating Json Report")
        else:
            logger.info("Cannot create json")

    def diff_slicer(self):
        self.get_diff()

        for added in range(self.num_of_added):
            self.added_tag.append((re.findall(r'\d+', self.differences["dictionary_item_added"][added]))[0])

        for removed in range(self.num_of_removed):
            self.removed_tag.append((re.findall(r'\d+', self.differences["dictionary_item_removed"][removed]))[0])

        for change in range(self.num_of_changes):

            change_on = list(self.differences["values_changed"].keys())[change];
            change_on = change_on[(len((re.findall(r"\d+", (list(self.differences["values_changed"].keys())[change])))[0]) + 10):];
            change_on = change_on[:-2]
            # print(change_on, "a")
            self.changed_field.append(change_on)

            if change_on == "person":
                self.asset_tag_person.append((re.findall(r"\d+", (list(self.differences["values_changed"].keys())[change])))[0])
                # print("Asset tag?",(re.findall(r"\d+", (list(self.differences["values_changed"].keys())[change])))[0])
                self.old_value_person.append(list(self.differences["values_changed"].values())[change]["old_value"])
                # print(list(self.differences["values_changed"].values())[change]["old_value"])
                self.new_value_person.append(list(self.differences["values_changed"].values())[change]["new_value"])
                # print(list(self.differences["values_changed"].values())[change]["new_value"])

            if change_on == "os_number":
                self.asset_tag_os_num.append((re.findall(r"\d+", (list(self.differences["values_changed"].keys())[change])))[0])
                self.old_value_os_num.append(list(self.differences["values_changed"].values())[change]["old_value"])
                self.new_value_os_num.append(list(self.differences["values_changed"].values())[change]["new_value"])

            if change_on not in ["person", "os_number"]:
                self.asset_tag_misc.append((re.findall(r"\d+", (list(self.differences["values_changed"].keys())[change])))[0])
                self.old_value_misc.append(list(self.differences["values_changed"].values())[change]["old_value"])
                self.new_value_misc.append(list(self.differences["values_changed"].values())[change]["new_value"])

    def pretty_diffs_xlsx(self):
        if self.check_if_changed() is None:
            self.diff_slicer()

            logger.info("Start to create Excel Report")
            report = Report(save_path=self.save_path)

            report.write_list_to_excel_with_sheets(sheet_name="person", save_name=self.filename, start_column="A", col_name="Asset Tag", lst1=self.asset_tag_person)
            report.write_list_to_excel_with_sheets(sheet_name="person", save_name=self.filename, start_column="B", col_name="Odgovorna osoba na pocetni datum", lst1=self.old_value_person)
            report.write_list_to_excel_with_sheets(sheet_name="person", save_name=self.filename, start_column="C", col_name="Odgovorna osoba na krajnji datum", lst1=self.new_value_person)

            report.write_list_to_excel_with_sheets(sheet_name="os_number", save_name=self.filename, start_column="A", col_name="Asset Tag", lst1=self.asset_tag_os_num)
            report.write_list_to_excel_with_sheets(sheet_name="os_number", save_name=self.filename, start_column="B", col_name="broj osnovnog sredstva na pocetni datum", lst1=self.old_value_os_num)
            report.write_list_to_excel_with_sheets(sheet_name="os_number", save_name=self.filename, start_column="C", col_name="broj osnovnog sredstva na krajnji datum", lst1=self.new_value_os_num)

            report.write_list_to_excel_with_sheets(sheet_name="misc", save_name=self.filename, start_column="A", col_name="Asset Tag", lst1=self.asset_tag_misc)
            report.write_list_to_excel_with_sheets(sheet_name="misc", save_name=self.filename, start_column="B", col_name="stara vrijednost", lst1=self.old_value_misc)
            report.write_list_to_excel_with_sheets(sheet_name="misc", save_name=self.filename, start_column="C", col_name="nova vrijednost", lst1=self.new_value_misc)

            logger.info("Ended creating Excel Report")
        else:
            logger.info("Cannot create Excel Report")


if __name__ == "__main__":
    my_diff = Diff("dict_from_snipe_data_11.10.2022", "dict_from_snipe_data_30.10.2022", save_name="g", save_path="results_cron/diff/").pretty_diffs_xlsx()
    # my_diff = Diff("dict_from_snipe_data_11.10.2022", "dict_from_snipe_data_10.10.2022", save_name="g",save_path="results_cron/diff/").pretty_diffs_xlsx()