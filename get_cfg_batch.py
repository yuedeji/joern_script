import os
import sys
from tqdm import tqdm

code_folder = "/home/yuedeji/firmware/bug_dataset/testsuites/Juliet_1.3/testcases"

output_home = "/home/yuedeji/firmware/bug_dataset/testsuites/Juliet_1.3/processed"

folder_list = os.listdir(code_folder)

print(folder_list)
print(len(folder_list))

cwe_list = ['416', '457', '415', '476']

for folder in folder_list:
#    if ("CWE119" not in folder) and ("CWE399" not in folder):
#        continue
    is_in = False
    for cwe in cwe_list:
#        print(cwe, folder)
        if cwe in folder:
            is_in = True
            break
    if is_in == False:
        continue

#    print("found one\n")

    folder_path = os.path.join(code_folder, folder)
    db_folder = os.path.join(folder_path, "." + folder.split('_')[0]+"DB")

    output_folder = os.path.join(output_home, folder)

    if not os.path.isdir(output_folder):
        os.system("mkdir %s" %(output_folder))

    uid_file = os.path.join(output_folder, "uid2funcinfo.csv")
#    if os.path.isfile(uid_file):
#        continue

    cmd = "python get_code.py %s %s" %(db_folder, output_folder)
    print(cmd)
    os.system(cmd)


