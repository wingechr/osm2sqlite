#!/usr/bin/env python3
# coding=utf-8
"""SCRIPT DOCSTRING"""

import sys
import argparse
import logging

def main(*args, **kwargs):
    pass

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--loglevel', '-v', default='info', help='set output verbosity')
    # add more arguments here
    kwargs = vars(ap.parse_args())
    logging.basicConfig(format='[%(asctime)s %(levelname)s] %(message)s', level=kwargs.pop('loglevel', 'info').upper())
    try:
        res = main(**kwargs)
        # TODO: if result has data: write to stdout
        rc = 0 if res else 1
    except KeyboardInterrupt:
        logging.info('Quit')
        rc = 1
    sys.exit(rc)