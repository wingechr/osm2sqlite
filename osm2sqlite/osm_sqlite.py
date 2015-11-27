#!/usr/bin/env python3
# coding=utf-8
"""Converting local compressed osm file (*.osm.bz2) to sqlite3 database (*.db)."""

import sys
import argparse
import logging
from osm2sqlite import osm


def _get_args_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument('--loglevel', '-v', default='info', help='set output verbosity')
    ap.add_argument('input_file', help='input path (.osm.bz2)')
    ap.add_argument('output_file', help='output path (.db)')
    return ap


def main(**kwargs):
    """MAIN

    .. argparse::
        :module: osm2sqlite.osm_sqlite
        :func: _get_args_parser
        :prog: NAME
    """
    with osm.SqliteOutput(kwargs['output_file']) as output:
        osm.parse_osm(kwargs['input_file'], output, clean_str=osm.default_clean_str)

if __name__ == '__main__':
    ap_kwargs = vars(_get_args_parser().parse_args())
    logging.basicConfig(format='[%(asctime)s %(levelname)s] %(message)s', level=ap_kwargs.pop('loglevel', 'info').upper())
    try:
        main(**ap_kwargs)
        rc = 0
    except KeyboardInterrupt:
        logging.info('User terminated')
        rc = 1
    except Exception as e:
        logging.error(e)
        rc = 2
    sys.exit(rc)
