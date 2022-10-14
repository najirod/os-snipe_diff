import os
from openpyxl import load_workbook
from openpyxl import Workbook
from datetime import date


class Report:
    def __init__(self, save_path=None):
        self.wb_result = Workbook()

        self.default_path =  os.getenv("export_results_path_test")
        self.save_path = save_path
        if save_path is None:
            self.export_results_path = self.default_path
        else:
            self.export_results_path = self.save_path

    # upis podataka u excel
    def write_list_to_excel(self, save_name="result", start_column="A", col_name="...",  lst1=None):
        sheet_ranges_result = self.wb_result.active
        cell_n = 2
        for item in lst1:
            if item is None:
                pass
            else:
                sheet_ranges_result[start_column + "1"] = col_name
                sheet_ranges_result[start_column + str(cell_n)] = item
                cell_n += 1

                self.wb_result.save(self.export_results_path + save_name + ".xlsx")
"""
    def generate_matching_xlsx(self, check):
        print("g started")
        self.write_list_to_excel(save_name="matching",start_column="A",col_name="os_num",lst1=check.matching)
        self.write_list_to_excel(save_name="matching", start_column="B", col_name="snipe_name", lst1=check.aseet_names_from_snipe_that_match)
        self.write_list_to_excel(save_name="matching",start_column="C",col_name="acc_name", lst1=check.asset_names_from_os_that_match)
        self.write_list_to_excel(save_name="matching",start_column="D",col_name="Asset_number",lst1=check.asset_tags_match)

    def generate_non_matching_xlsx(self,check):
        print("pocelo je")
        self.write_list_to_excel(save_name="non_matching",start_column="A",col_name="os_num",lst1=check.non_matching)
        self.write_list_to_excel(save_name="non_matching", start_column="B",col_name="os_name",lst1=check.asset_names_from_os_that_dont_match)


    def generate_rest_xlsx(self,check):
        self.write_list_to_excel(save_name="rest", start_column="A", col_name="asset_tages", lst1=check.rest_tags)
        self.write_list_to_excel(save_name="rest", start_column="B", col_name="name_from_snipe", lst1=check.rest_names)

"""