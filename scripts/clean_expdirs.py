#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.

from argparse import ArgumentParser
import yaml
import os
import shutil
from sys import stderr


def parse_args():
    p = ArgumentParser(
        description="""Clean experiment directories.
        The script does the following:
        1. Removes directory of failed experiments.
        An experiment is considered failed if result.yaml
        exists but train_loss is an empty sequence (nothing was saved).
        2. Deletes empty train/dev/test output files.""")
    p.add_argument("expdirs", nargs='+', type=str)
    p.add_argument("--remove-empty", action="store_true",
                   help="Remove directories without a model file. "
                   "Use this only if there are no experiments "
                   "currently running.")
    p.add_argument("--remove-result-empty", action="store_true")
    p.add_argument("--dry-run", action="store_true",
                   help="Simulate run without deleting anything")
    return p.parse_args()


def delete_dir(expdir, dry_run=False):
    stderr.write("Deleting directory {}\n".format(expdir))
    if dry_run is False:
        shutil.rmtree(expdir)


def is_empty_expdir(expdir):
    # no model file
    return all(not fn.startswith('model') for fn in os.listdir(expdir))


def is_result_empty(expdir):
    result_fn = os.path.join(expdir, 'result.yaml')
    if not os.path.exists(result_fn):
        return True
    with open(os.path.join(expdir, 'result.yaml')) as f:
        result = yaml.load(f)
    return len(result['train_loss']) == 1


def delete_empty_outputs(expdir, dry_run=False):
    for typ in ['train', 'dev', 'test']:
        fn = os.path.join(expdir, '{}.out'.format(typ))
        if os.path.exists(fn):
            with open(fn) as f:
                content = f.read()
            if not content.strip():
                stderr.write("Deleting file: {}\n".format(fn))
                if dry_run is False:
                    os.remove(fn)
                acc_fn = os.path.join(expdir, '{}.word_accuracy'.format(typ))
                if os.path.exists(acc_fn):
                    stderr.write("Deleting file: {}\n".format(acc_fn))
                    if dry_run is False:
                        os.remove(acc_fn)


def delete_two_column_outputs(expdir, dry_run=False):
    for typ in ['train', 'dev', 'test']:
        fn = os.path.join(expdir, '{}.out'.format(typ))
        if not os.path.exists(fn):
            continue
        with open(fn) as f:
            first = next(f)
            if len(first.strip().split('\t')) == 2:
                stderr.write("{} has only two columns (tags missing)".format(fn))
                if dry_run is False:
                    os.remove(fn)


def main():
    args = parse_args()
    for expdir in args.expdirs:
        if is_empty_expdir(expdir):
            if args.remove_empty:
                delete_dir(expdir, args.dry_run)
            continue
        if is_result_empty(expdir):
            if args.remove_result_empty:
                delete_dir(expdir, args.dry_run)
            continue
        delete_empty_outputs(expdir, args.dry_run)

if __name__ == '__main__':
    main()
