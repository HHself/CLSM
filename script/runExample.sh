#!/bin/bash

#run dssm

#nagitive samples 
nagnum=128

input_dir=../sample-data/ 
output_dir=../output/

# the input docs for training
doc_sc=${input_dir}doc_info.txt

echo "============= generate train doc (doc, flag) ============"

doc_vec=${output_dir}doc_vec.txt
doc_flag=${output_dir}doc_flag.txt

python ../py/tools.py $doc_sc $nagnum $doc_vec $doc_flag

wc -l "{output_dir}doc_flag.txt" 
echo "================== training DSSM ========================"

/opt/MATLAB/R2012a/bin/matlab <../ma/runtrain.m > mat.out


echo "====================== End =============================="
