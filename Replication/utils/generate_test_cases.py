# import os
# import glob
# import sys
# import pandas as pd
#
# def generate_testcase_file_path(file_path):
#     df = pd.read_csv(file_path)
#     testcase_paths = df['testcase_path'].values
#     return testcase_paths
#
# if __name__ == "__main__":
#     testcase_csv_path = '../testcases.csv'
#     print(generate_testcase_file_path(testcase_csv_path))
