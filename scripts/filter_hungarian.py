#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.

from argparse import ArgumentParser


def parse_args():
    p = ArgumentParser()
    p.add_argument('to_filter', type=str)
    p.add_argument('filter', type=str)
    return p.parse_args()


def main():
    args = parse_args()
    with open(args.filter) as f:
        filter_ = set(l.strip() for l in f)
    with open(args.to_filter) as f:
        for line in f:
            if line.strip() in filter_:
                print(line.rstrip('\n'))

if __name__ == '__main__':
    main()
