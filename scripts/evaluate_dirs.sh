#! /bin/sh
#
# evaluate_dirs.sh
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
    if [ ! -f $exp_dir/train.word_accuracy ] || [ $exp_dir/model -nt $exp_dir/train.word_accuracy ]; then
        echo "----------------------"
        echo "EXPERIMENT $exp_dir"
        echo "   Evaluating train file: $(basename $train_file)"
        python $INFERENCE_SRC -e $exp_dir -t $train_file --override-param batch_size=16 > $exp_dir/train.out
        if [ $? -eq 0 ]; then
            paste $train_file <( cut -f2 $exp_dir/train.out ) | sed 's/ //g' | awk 'BEGIN{FS="\t"}{if($2==$NF)c++;s++}END{print c/s}' > $exp_dir/train.word_accuracy
            echo "   " $(cat $exp_dir/train.word_accuracy)
        else
            echo "   Inference failed"
        fi
    fi

    dev_file=$(grep ^dev_file $exp_dir/config.yaml)
    dev_file=${dev_file#dev_file: }
    if [ ! -f $exp_dir/dev.batch16.word_accuracy ] || [ $exp_dir/model -nt $exp_dir/dev.batch16.word_accuracy ]; then
        echo "   Evaluating dev file: $(basename $dev_file)"
        python $INFERENCE_SRC -e $exp_dir -t $dev_file --override-param batch_size=16 > $exp_dir/dev.batch16.out
        if [ $? -eq 0 ]; then
            paste $dev_file <( cut -f2 $exp_dir/dev.batch16.out ) | sed 's/ //g' | awk 'BEGIN{FS="\t"}{if($2==$NF)c++;s++}END{print c/s}' > $exp_dir/dev.batch16.word_accuracy
            echo "   " $(cat $exp_dir/dev.batch16.word_accuracy)
        else
            echo "   Inference failed"
        fi
    fi
done

