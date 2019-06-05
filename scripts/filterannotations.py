#!/usr/bin/env python3

import os
import sys
import json

from collections import Counter
from logging import warning, error, info


MAX_REGISTER = 10


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('-a', '--ascii', default=False, action='store_true')
    ap.add_argument('-m', '--min-count', default=10, type=int,
                    help='minimum register label count')
    ap.add_argument('-p', '--pretty', default=False, action='store_true',
                    help='pretty-print JSON')
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

    filtered = {}
    for doc_id, doc_data in data.items():
        if not doc_id.isdigit():
            warning('non-intenger doc_id: "{}"'.format(doc_id))
        registers = get_registers(doc_data)
        if not registers:
            error('no registers for {}'.format(doc_id))
        elif len(registers) > 1:
            info('filtering {}: {} registers'.format(doc_id, len(registers)))
        else:
            filtered[doc_id] = doc_data
    print('Remove hybrids: filtered documents from {} to {}'.format(
        len(data), len(filtered)), file=sys.stderr)
    data, filtered = filtered, {}

    register_count = Counter()
    for doc_id, doc_data in data.items():
        for r in get_registers(doc_data):
            register_count[r] += 1
    filtered_register = set()
    for label, count in register_count.items():
        if count < options.min_count:
            print('Remove rare: filtering out {} ({} examples)'.format(
                label, count), file=sys.stderr)
            filtered_register.add(label)
    for doc_id, doc_data in data.items():
        registers = get_registers(doc_data)
        if any(r for r in registers if r not in filtered_register):
            filtered[doc_id] = doc_data
    print('Remove rare: filtered documents from {} to {}'.format(
        len(data), len(filtered)), file=sys.stderr)

    return filtered


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        filtered = filter_file(fn, args)
        if not args.pretty:
            print(json.dumps(filtered, ensure_ascii=args.ascii))
        else:
            print(json.dumps(filtered, indent=4, sort_keys=True,
                             ensure_ascii=args.ascii))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
