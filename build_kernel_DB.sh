#!/bin/bash
kernel_home="/home/yuedeji/linux_kernel"
kernel_file="/home/yuedeji/linux_kernel/vlc-2.2.4"

ant
ant tools

rm -rf ${kernel_home}/.kernelDB
java -jar bin/joern.jar ${kernel_file} -outdir ${kernel_home}/.kernelDB

# Taint sources 

java -jar bin/argumentTainter.jar -dbdir ${kernel_home}/.kernelDB taint_source 1
java -jar bin/argumentTainter.jar -dbdir ${kernel_file}/.kernelDB second_taint_source 0
java -jar bin/argumentTainter.jar -dbdir ${kernel_home}/.kernelDB interproc_callee 0
