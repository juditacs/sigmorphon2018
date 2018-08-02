#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 Judit Acs <judit@sch.bme.hu>
#
# Distributed under terms of the MIT license.
import os
import yaml
from sys import stderr

import torch
import numpy as np
import pandas as pd


def compute_sparsity(model_fn, threshold=10e-3):
    is_zero = 0
    non_zero = 0
    for name, tensor in torch.load(model_fn).items():
        m = tensor.cpu().numpy()
        close = len(np.where(np.abs(m) <= threshold)[0])
        is_zero += close
        non_zero += (m.size - close)
    return is_zero, non_zero, is_zero / (is_zero + non_zero)


def get_min_loss(row):
    try:
        min_idx, min_dev_loss = min(enumerate(row['dev_loss']), key=lambda x: x[1])
        min_train_loss = row['train_loss'][min_idx]
        row['min_dev_loss'] = min_dev_loss
        row['min_train_loss'] = min_train_loss
    except ValueError:
        row['min_dev_loss'] = row['min_train_loss'] = None
    return row


def extract_language_name(field):
    fn = field.split('/')[-1]
    if 'dev' in fn:
        return '-'.join(fn.split('-')[:-1])
    return '-'.join(fn.split('-')[:-2])


def load_experiment_dir(basedir, include_sparsity=False):
    experiments = []
    for subdir in os.scandir(basedir):
        exp_d = {}
        with open(os.path.join(subdir.path, "config.yaml")) as f:
            exp_d.update(yaml.load(f))
        res_fn = os.path.join(subdir.path, "result.yaml")
        if os.path.exists(res_fn):
            with open(os.path.join(subdir.path, "result.yaml")) as f:
                exp_d.update(yaml.load(f))
        else:
            continue
        train_acc_path = os.path.join(subdir.path, "train.word_accuracy")
        if os.path.exists(train_acc_path):
            with open(train_acc_path) as f:
                exp_d['train_acc'] = float(f.read())
        else:
            stderr.write("Train accuracy file does not exist in dir: {}\n".format(subdir.path))
        dev_acc_path = os.path.join(subdir.path, "dev.word_accuracy")
        if os.path.exists(dev_acc_path):
            with open(dev_acc_path) as f:
                exp_d['dev_acc'] = float(f.read())
        else:
            stderr.write("Dev accuracy file does not exist in dir: {}\n".format(subdir.path))
        if include_sparsity:
            exp_d['sparsity'] = compute_sparsity(os.path.join(subdir.path, "model"), 10e-4)
        experiments.append(exp_d)
    experiments = pd.DataFrame(experiments)
    if include_sparsity:
        experiments['sparsity_ratio'] = experiments['sparsity'].apply(lambda x: x[2])
    experiments['language'] = experiments.dev_file.apply(extract_language_name)
    experiments = experiments.apply(get_min_loss, axis=1)
    experiments = experiments[experiments['dev_acc'].notnull()]
    experiments = experiments[experiments['dev_loss'].notnull()]
    experiments['train_size'] = experiments['train_file'].apply(lambda fn: fn.split('-')[-1])
    return experiments
