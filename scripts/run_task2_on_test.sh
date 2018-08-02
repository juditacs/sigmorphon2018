#! /bin/sh
#
# run_task2_on_test.sh
# Copyright (C) 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.
#


INFERENCE_SRC=../deep-morphology/deep_morphology/inference.py


for exp_dir in "$@"; do
    if [ ! -f $exp_dir/config.yaml ]; then
        echo "$exp_dir is not an experiment dir"
        continue
    fi
    if [ ! -f $exp_dir/test.out ] || [ $exp_dir -nt $exp_dir/test.out ]; then
        train_file=$(grep ^train_file $exp_dir/config.yaml)
        train_file=${train_file#train_file: }
        train_dir=$(dirname $train_file)
        lang=$(basename $train_file | cut -f1 -d"-")
        track=$(basename $train_file | cut -f2 -d"-")
        test_file=$train_dir/../testsets/${lang}-${track}-covered
        echo "Running inference in $exp_dir"
        echo "   Test file: $test_file"
        python $INFERENCE_SRC -e $exp_dir -t $test_file > $exp_dir/test.out
    fi
done
