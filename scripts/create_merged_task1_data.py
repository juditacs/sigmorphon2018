#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.

from argparse import ArgumentParser
import os


def parse_args():
    p = ArgumentParser()
    p.add_argument('input_files', nargs='+', type=str)
    return p.parse_args()


def main():
    args = parse_args()
    for path in args.input_files:
        lang = '-'.join(os.path.basename(path).split('-')[:-2])
        with open(path) as f:
            for line in f:
                lemma, inflected, tags = line.rstrip('\n').split('\t')
                tags = tags.split(';')
                tags.append('LANG:{}'.format(lang))
                print('{}\t{}\t{}'.format(lemma, inflected, ';'.join(tags)))

if __name__ == '__main__':
    main()
