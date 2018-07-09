#! /bin/sh
#
# run_task2_track1.sh
# Copyright (C) 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.
#

TRAIN_PY=$1
CONFIG=$2

for train in "${@:3}" ; do
    lang=$(basename $train | cut -f1 -d"-")
    train_dir=$(dirname $train)
    dev=$train_dir/../devsets/${lang}-uncovered
    echo $train
    python $TRAIN_PY -c $CONFIG --train $train --dev $dev
done
