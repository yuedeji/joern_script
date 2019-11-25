import os
import sys

code_folder = "/home/yuedeji/firmware/bug_dataset/testsuites/Juliet_1.3/testcases"

folder_list = os.listdir(code_folder)

print(folder_list)
print(len(folder_list))

for folder in folder_list:
    folder_path = os.path.join(code_folder, folder)
    out_file = "." + folder.split('_')[0]+"DB"

    cmd = "./build_db.sh " + folder_path + " " + out_file
    print(cmd)
    os.system(cmd)


