#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.

from argparse import ArgumentParser
from sys import stderr
import yaml
import os
import shutil


def parse_args():
    p = ArgumentParser()
    p.add_argument("-m", "--min-epoch", type=int, default=5)
    p.add_argument("-d", "--delete-dir", action="store_true")
    p.add_argument("-l", "--log-dirs", type=str,
                   help="log expdirs and train files to file")
    p.add_argument("exp_dirs", nargs="+", type=str)
    return p.parse_args()


def main():
    args = parse_args()
    short_exp_dirname = []
    for expdir in args.exp_dirs:
        with open(os.path.join(expdir, "result.yaml")) as f:
            res = yaml.load(f)
        epochs = len(res['train_loss'])
        if epochs >= args.min_epoch:
            continue
        with open(os.path.join(expdir, "config.yaml")) as f:
            config = yaml.load(f)
        train_file = config['train_file']
        short_exp_dirname.append((expdir, train_file))
        if args.delete_dir:
            stderr.write("Deleting directory: {}\n".format(expdir))
            shutil.rmtree(expdir)
    if args.log_dirs:
        with open(args.log_dirs, 'w') as f:
            f.write("\n".join(
                "{}\t{}".format(e, t) for e, t in short_exp_dirname) + "\n")

if __name__ == '__main__':
    main()
