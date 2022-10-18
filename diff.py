from deepdiff import DeepDiff
import json
import os
import re

import sys

#from setuptools.sandbox import save_path

from ExcelReport import Report

from dotenv import load_dotenv


class Diff:
    def __init__(self, filename1, filename2, save_path=None, save_name="file"):
        root_path = (sys.path[1] + "/") #/Users/dpustahija1/PycharmProjects/os-snipe_diff/
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
        self.asset_tag = []
        self.new_value = []
        self.old_value = []

    def check_if_changed(self):
        with open(self.path + self.file1 + ".json", "r", encoding="utf-8") as json1:
            js1 = json.load(json1)
        with open(self.path + self.file2 + ".json", "r", encoding="utf-8") as json2:
            js2 = json.load(json2)

        self.differences = dict(DeepDiff(js1, js2))
        # print(self.differences)
        if self.differences == {}:
            print("diff, check_if_changed", "0")
            return "0"

    def get_diff(self):
        with open(self.path + self.file1 + ".json", "r", encoding="utf-8") as json1:
            js1 = json.load(json1)
        with open(self.path + self.file2 + ".json", "r", encoding="utf-8") as json2:
            js2 = json.load(json2)

        self.differences = dict(DeepDiff(js1, js2))
        # print(self.differences)
        if self.differences != {}:
            self.num_of_changes = len(self.differences["values_changed"])
        else:
            pass
        # print(self.differences)

    def create_json(self):
        self.get_diff()
        with open(self.export_results_path_diff + 'diffs.json', 'w') as write_file:
            json.dump(self.differences, write_file)

    def pretty_diffs_xlsx(self):
        self.get_diff()

        for change in range(self.num_of_changes):
            self.asset_tag.append((re.findall(r"\d+", (list(self.differences["values_changed"].keys())[change])))[0])
            # print((re.findall(r"\d+", (list(self.differences["values_changed"].keys())[change])))[0])
            self.old_value.append(list(self.differences["values_changed"].values())[change]["old_value"])
            # print(list(self.differences["values_changed"].values())[change]["old_value"])
            self.new_value.append(list(self.differences["values_changed"].values())[change]["new_value"])
            # print(list(self.differences["values_changed"].values())[change]["new_value"])

        report = Report(save_path=self.save_path)
        report.write_list_to_excel(save_name=self.filename, start_column="A", col_name="Asset Tag", lst1=self.asset_tag)
        report.write_list_to_excel(save_name=self.filename, start_column="B", col_name="Odgovorna osoba na pocetni datum", lst1=self.old_value)
        report.write_list_to_excel(save_name=self.filename, start_column="C", col_name="Odgovorna osoba na krajnji datum", lst1=self.new_value)


        # print(self.asset_tag)
        # print(self.old_value)
        # print(self.new_value)
        # print(self.num_of_changes)
        # print("1" , self.differences["values_changed"])
        # print("2", type(list(self.differences["values_changed"].keys())[0]))


        # print(list(self.differences["values_changed"].values())[0]["new_value"])



if __name__ == "__main__":
    my_diff = Diff("dict_from_snipe_data_10.10.2022", "dict_from_snipe_data_11.10.2022", save_name="g", save_path="results_cron/diff/").pretty_diffs_xlsx()
    #my_diff =print( "test",Diff("dict_from_snipe_data_11.10.2022", "dict_from_snipe_data_25.10.2022", save_name="g", save_path="results_cron/diff/").check_if_changed())