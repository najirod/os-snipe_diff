from deepdiff import DeepDiff
import json
import os

from dotenv import load_dotenv


class Diff:
    def __init__(self, filename1, filename2):
        load_dotenv()
        self.file1 = filename1
        self.file2 = filename2
        self.path = os.getenv("diff_path")
        self.export_results_path = os.getenv("export_results_path_test")
        self.differences = {}

    def get_diff(self):
        with open(self.path + self.file1 + ".json", "r") as json1:
            js1 = json.load(json1)
        with open(self.path + self.file2 + ".json", "r") as json2:
            js2 = json.load(json2)

        self.differences = dict(DeepDiff(js1, js2))
        print(self.differences)

        with open(self.export_results_path + 'diffs.json', 'w') as write_file:
            json.dump(self.differences, write_file)


if __name__ == "__main__":
    my_diff = Diff("test1", "test2")
    my_diff.get_diff()
