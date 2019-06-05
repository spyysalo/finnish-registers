#!/usr/bin/env python3

import os
import sys
import json

from collections import Counter
from logging import warning, error, info

from sklearn.model_selection import train_test_split


MAX_REGISTER = 10


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-a', '--ascii', default=False, action='store_true')
    ap.add_argument('-r', '--ratio', default=0.8, type=float)
    ap.add_argument('-s', '--stratify', default=False, action='store_true')
    ap.add_argument('-i', '--ignore', metavar='FILE', default=None,
                    help='ignore document IDs in FILE')
    ap.add_argument('data', metavar='JSON', help='annotations')
    ap.add_argument('out1')
    ap.add_argument('out2')
    return ap


def ids_and_labels(data):
    ids, labels = [], []
    for doc_id, doc_data in data.items():
        label = doc_data['register-1']
        if any(i for i in range(2, MAX_REGISTER)if
               'register-{}'.format(i) in doc_data):
            raise ValueError(
                'multiple registers for {} (did you run filterannotations?)'.\
                format(doc_id))
        ids.append(doc_id)
        labels.append(label)
    return ids, labels


def write_subset(data, ids, out, options):
    subset = { k: v for k, v in data.items() if k in ids }
    print(json.dumps(subset, ensure_ascii=options.ascii), file=out)
    print('wrote {} documents in {}'.format(len(subset), out.name),
          file=sys.stderr)


def read_ids(fn):
    ids = []
    with open(fn) as f:
        for l in f:
            ids.append(l.strip())
    return ids


def main(argv):
    args = argparser().parse_args(argv[1:])
    if not 0 < args.ratio < 1:
        raise ValueError('must have 0 < RATIO < 1')
    with open(args.data) as f:
        data = json.load(f)

    if args.ignore is not None:
        ignore = set(read_ids(args.ignore))
        full_count = len(data)
        data = { k: v for k, v in data.items() if k not in ignore }
        print('Ignore: filtered documents from {} to {}'.format(
            full_count, len(data), file=sys.stderr))

    ids, labels = ids_and_labels(data)

    label_count = Counter()
    for l in labels:
        label_count[l] += 1
    rare_label_ids = []
    rare_labels = [l for l in label_count if label_count[l] < 10]
    if any(rare_labels) and args.stratify:
        warning('Stratify with labels with fewer than 2 instances: {}'.format(
            ', '.join(rare_labels)))
        rare_label_ids = [i for i, l in zip(ids, labels) if l in rare_labels]
        filtered_ids, filtered_labels = [], []
        for i, l in zip(ids, labels):
            if l not in rare_labels:
                filtered_ids.append(i)
                filtered_labels.append(l)
        ids, labels = filtered_ids, filtered_labels
        warning('Placing {} documents with rare labels in first set'.format(
            len(rare_label_ids)))

    print(len(ids))
    print(len(labels))

    stratify = labels if args.stratify else None
    ids1, ids2, labels1, labels2 = train_test_split(
        ids, labels, train_size=args.ratio, stratify=stratify)

    ids1 = ids1 + rare_label_ids

    with open(args.out1, 'w') as out:
        write_subset(data, ids1, out, args)
    with open(args.out2, 'w') as out:
        write_subset(data, ids2, out, args)

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
