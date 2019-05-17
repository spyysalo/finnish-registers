#!/usr/bin/env python3

import os
import sys
import json

from logging import warning


MAX_REGISTER = 10


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
            registers = []
            for i in range(MAX_REGISTER):
                key = 'register-{}'.format(i)
                if key in doc_data:
                    register = doc_data[key]
                    if not register or register.isspace():
                        warning('empty {} in {}'.format(key, doc_id))
                    registers.append(register)
            print('{}\t{}'.format(doc_id, ', '.join(sorted(registers))))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
