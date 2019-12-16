import os
import sys
import csv

data_folder = "/home/yuedeji/firmware/bug_dataset/testsuites/Juliet_1.3/processed"

def get_label(input_file, output_file):
    fp_out = open(output_file, "w")
    num_positive = 0
    num_negative = 0
    with open(input_file, "r") as fp:
        for line in csv.reader(fp):
            if "bad" in line[-1].lower():
                fp_out.write("1\n")
                num_positive += 1
            else:
                fp_out.write("0\n")
                num_negative += 1
    return num_positive, num_negative

fp_sum = open("label_summary.csv", "w")
fp_sum.write("CWE,positive,negative,total,positive / negative\n")
for dir_path, _, files in os.walk(data_folder):
    for file_one in files:
        if file_one == "uid2funcinfo.csv":
            uid_file = os.path.join(dir_path, file_one)
            output_file = os.path.join(dir_path, "graph_label.csv")

            p, n = get_label(uid_file, output_file)
            fp_sum.write(dir_path + ',' + str(p) + ',' + str(n) + ',' + str(p + n) + ',' + str(p * 1.0 / n) + '\n')

fp_sum.close()
