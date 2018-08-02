#! /bin/sh
#
# evaluate_every_model_task2.sh
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

    if [ ! -f $exp_dir/model.epoch_0000 ]; then
        continue
    fi

    for model in $(ls $exp_dir/model*); do
        epoch=${model#*model.}
        if [ ! -f $exp_dir/dev.word_accuracy.$epoch ]; then
            echo "Dir: $exp_dir, model: model.$epoch"
            lang=$(basename $dev_file | cut -f1 -d"-")
            covered=$(dirname $dev_file)/${lang}-track1-covered
            python $INFERENCE_SRC -e $exp_dir -t $covered --model $model > $exp_dir/dev.out.$epoch
            paste $exp_dir/dev.out.$epoch $dev_file | grep "_" | awk 'BEGIN{FS="\t"}{if($1==$4)c++;s++}END{print c/s}' > $exp_dir/dev.word_accuracy.$epoch
            cat ${exp_dir}/dev.word_accuracy.$epoch
        fi
    done
done
