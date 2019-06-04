#!/usr/bin/env python3

import os
import sys
import json

from collections import Counter
from logging import warning, error, info


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('file', metavar='JSON', nargs='+', help='annotations')
    return ap


def get_registers(doc_data):
    registers = []
    for i in range(MAX_REGISTER):
        key = 'register-{}'.format(i)
        if key in doc_data:
            registers.append(doc_data[key])
    return registers


def filter_file(fn, options):
    with open(fn) as f:
        data = json.load(f)
    for doc_id, doc_data in data.items():
        registers = get_registers(doc_data)
        if not registers:
            error('no registers for {}'.format(doc_id))
        elif len(registers) > 1:
            print('hybrid:\t{}'.format(doc_id))
            

def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        find_hybrids(fn, args)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
