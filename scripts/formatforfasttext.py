#!/usr/bin/env python3

import os
import sys
import json

from logging import warning, error


MAX_REGISTER = 10


def get_registers(doc_data):
    registers = []
    for i in range(MAX_REGISTER):
        key = 'register-{}'.format(i)
        if key in doc_data:
            registers.append(doc_data[key])
    return registers


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('file', metavar='JSON', nargs='+', help='annotations')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        with open(fn) as f:
            data = json.load(f)
        for doc_id, doc_data in data.items():
            registers = get_registers(doc_data)
            labels = [
                '__label__{}'.format(r.replace(' ','_'))
                for r in registers
            ]
            try:
                text = doc_data['text']
            except KeyError:
                error('no text for {}'.format(doc_id))
                continue
            print(' '.join(labels + [text]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
