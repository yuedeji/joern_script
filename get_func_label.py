import os
import sys
import csv

data_folder = "/home/yuedeji/firmware/bug_dataset/testsuites/Juliet_1.3/processed"

def get_label(input_file, output_file):

    fp_out = open(output_file, "w")
    with open(input_file, "r") as fp:
        for line in csv.reader(fp):
            if "bad" in line[-1].lower():
                fp_out.write("1\n")
            else:
                fp_out.write("0\n")


for dir_path, _, files in os.walk(data_folder):
    for file_one in files:
        if file_one == "uid2funcinfo.csv":
            uid_file = os.path.join(dir_path, file_one)
            output_file = os.path.join(dir_path, "graph_label.csv")

            get_label(uid_file, output_file)
