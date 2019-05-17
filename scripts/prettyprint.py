#!/usr/bin/env python3

import os
import sys
import json


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
            print('{')
            for i, (doc_id, doc_data) in enumerate(data.items()):
                maybe_comma = ',' if i < len(data)-1 else ''                
                print('    {}: {}{}'.format(
                    json.dumps(doc_id, ensure_ascii=False),
                    json.dumps(doc_data, ensure_ascii=False),
                    maybe_comma
                ))
            print('}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
