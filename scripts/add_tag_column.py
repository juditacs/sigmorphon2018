#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.

from argparse import ArgumentParser
import yaml
import os
from sys import stderr


def parse_args():
    p = ArgumentParser()
    p.add_argument('expdirs', nargs='+')
    return p.parse_args()


def add_tag_column_if_needed(input_fn, output_fn):
    if not os.path.exists(output_fn):
        return
    with open(output_fn) as f:
        outputs = []
        for line in f:
            outputs.append(line.rstrip("\n").split("\t"))
    if len(outputs[0]) == 3:
        # has tags
        return
    with open(input_fn) as f:
        inputs = []
        for line in f:
            inputs.append(line.rstrip("\n").split("\t"))
    delete = any(' ' in sample[0] for sample in inputs)
    if delete:
        print("Should delete", output_fn)
        acc_file = output_fn.rstrip('.out') + '.word_accuracy'
        print(acc_file)
        os.remove(acc_file)
        os.remove(output_fn)
        return
    print("Now replacing", output_fn)
    assert len(inputs) == len(outputs)
    for i, (lemma, infl, tags) in enumerate(inputs):
        try:
            assert lemma == outputs[i][0]
        except AssertionError:
            print(lemma, infl, tags, outputs[i])
            raise
        outputs[i].append(tags)
    with open(output_fn, 'w') as f:
        for outp in outputs:
            f.write("{}\t{}\t{}\n".format(*outp))


def main():
    args = parse_args()
    for expdir in args.expdirs:
        config_fn = os.path.join(expdir, 'config.yaml')
        if not os.path.exists(config_fn):
            stderr.write("No config.yaml in {}\n".format(config_fn))
            continue
        with open(config_fn) as f:
            config = yaml.load(f)
        data_dir = os.path.dirname(config['train_file'])

        # train file
        train_input = config['train_file']
        train_output = os.path.join(expdir, 'train.out')
        add_tag_column_if_needed(train_input, train_output)

        # dev file
        dev_input = config['dev_file']
        dev_output = os.path.join(expdir, 'dev.out')
        add_tag_column_if_needed(dev_input, dev_output)

        # test file
        test_input = os.path.join(
            data_dir, '{}-covered-test'.format(config['language']))
        test_output = os.path.join(expdir, 'test.out')
        add_tag_column_if_needed(test_input, test_output)


if __name__ == '__main__':
    main()
