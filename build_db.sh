#!/bin/bash

#code_home="/home/yuedeji/firmware/bug_dataset/testsuites/Juliet_1.3"
#out_file=".juliet1.3DB"

code_home=$1
out_file=$2

#echo $code_home
#echo $out_file
#exit
#code_home="/home/yuedeji/firmware/bug_dataset/testsuites/100"
#out_file=".100DB"

ant
ant tools

rm -rf ${code_home}/$out_file
java -jar bin/joern.jar ${code_home} -outdir ${code_home}/${out_file}

# Taint sources 

java -jar bin/argumentTainter.jar -dbdir ${code_home}/$out_file taint_source 1
java -jar bin/argumentTainter.jar -dbdir ${code_home}/$out_file second_taint_source 0
java -jar bin/argumentTainter.jar -dbdir ${code_home}/$out_file interproc_callee 0
