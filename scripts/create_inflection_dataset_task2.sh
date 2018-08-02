#! /bin/sh
#
# create_inflection_dataset_task2.sh
# Copyright (C) 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.
#


indir=$1
outdir=$2

lower_script=/mnt/permanent/home/judit/projects/ulm/scripts/preprocessing/lower.py

mkdir -p $outdir/trainsets
mkdir -p $outdir/devsets

for train in $indir/trainsets/*; do
    fn=$(basename $train)
    paste <(cut -f2 $train ) <(cut -f1 $train | python $lower_script ) <(cut -f3 $train) > $outdir/trainsets/$fn
done

for dev in $indir/devsets/*; do
    fn=$(basename $dev)
    paste <(cut -f2 $dev ) <(cut -f1 $dev | python $lower_script ) <(cut -f3 $dev) > $outdir/devsets/$fn
done
