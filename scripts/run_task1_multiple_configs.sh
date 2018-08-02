#! /bin/sh
#
# run_task1_multiple_configs.sh
# Copyright (C) 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.
#

TRAIN_PY=$1
CONFIG_DIR=$2

for config in $(ls $CONFIG_DIR/*); do
    short_config=$(basename $config)
    for train_fn in "${@:3}"; do
        fn=$(basename $train_fn)
        if [[ $fn = *"dev"* ]]; then
            continue
        fi
        dev_fn=${fn/train*/dev}
        dev_fn="$(dirname $train_fn)/$dev_fn"
        echo $short_config $train_fn $dev_fn
        python3 $TRAIN_PY -c $config --train-file $train_fn --dev-file $dev_fn
    done
done
