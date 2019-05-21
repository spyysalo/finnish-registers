#!/usr/bin/env python3

import os
import sys
import json

from logging import warning


def argparser():
    from argparse import ArgumentParser
    ap = ArgumentParser()
    ap.add_argument('dir', help='output directory')
    ap.add_argument('file', metavar='JSON', nargs='+', help='annotations')
    return ap


def main(argv):
    args = argparser().parse_args(argv[1:])
    for fn in args.file:
        with open(fn) as f:
            data = json.load(f)
        for doc_id, doc_data in data.items():
            try:
                text = doc_data['text']
            except KeyError:
                warning('missing text for {}, skipping'.format(doc_id))
                continue
            outfn = os.path.join(args.dir, '{}.txt'.format(doc_id))
            with open(outfn, 'w') as f:
                f.write(text)
            

if __name__ == '__main__':
    sys.exit(main(sys.argv))
