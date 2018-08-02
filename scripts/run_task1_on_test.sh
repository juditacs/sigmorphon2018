#! /bin/bash
#
# run_task1_on_test.sh
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
    train_file=$(grep ^train_file $exp_dir/config.yaml)
    train_file=${train_file#train_file: }

    dev_file=$(grep ^dev_file $exp_dir/config.yaml)
    dev_file=${dev_file#dev_file: }
    lang=$(basename $dev_file | sed 's/-dev//')
    test=$(dirname $dev_file)/${lang}-covered-test
    if [ -f $test ]; then
        if [ ! -f $exp_dir/test.out ] || [ $exp_dir/model -nt $exp_dir/test.out ]; then
            echo "   Experiment: $exp_dir"
            echo "   Train file: " $(basename $train_file)
            echo "   Running inference on test file: $(basename $test)"
            python $INFERENCE_SRC -e $exp_dir -t $test --override-param batch_size=32 2>/dev/null > $exp_dir/test.out
            echo "--------------------"
        fi
    fi
done

