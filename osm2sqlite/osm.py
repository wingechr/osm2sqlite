# coding=utf-8
"""Parse compressed osm (xlm) data (osm.bz2)"""

import sqlite3
import bz2
import logging
import os
import sys
from xml.etree import ElementTree

lib_path = sys.executable if getattr(sys, 'frozen', False) else __file__
lib_path = os.path.dirname(os.path.abspath(lib_path))


class SqliteOutput:
    """Store parsed osm data in sqlite database.
    """

    def __init__(self, db):
        """
        Args:
            db (str): Path to sqlite database file.
            sql_init (optional[str]): path to intial sql script to set up or empty tables.

        """
        self.db = db
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()
        # load init sql script
        with open(os.path.join(lib_path, 'data', 'osm_sqlite_create.sql')) as f:
            self.cur.executescript(f.read())
        # perfomance tweaks
        # see http://codereview.stackexchange.com/questions/26822/myth-busting-sqlite3-performance-w-pysqlite
        self.cur.execute("PRAGMA synchronous = OFF;")
        self.cur.execute("PRAGMA journal_mode = OFF;")
        self.cur.execute('PRAGMA foreign_keys = OFF;')
        self.cur.execute('PRAGMA ignore_check_constraints = TRUE;')
        self.cur.execute('PRAGMA encoding = "UTF-8;"')
        return self

    def __exit__(self, type, value, traceback):
        _ = type, value, traceback
        self.cur.execute('PRAGMA foreign_keys = ON;')
        self.cur.execute('PRAGMA ignore_check_constraints = FALSE;')
        self.cur.execute('PRAGMA integrity_check;')
        self.cur.execute('PRAGMA foreign_key_check;')
        self.cur.close()
        self.con.commit()
        self.con.close()

    def _execute(self, sql, args=None):
        """Wrap actual execution to continue parsing"""
        try:
            self.cur.execute(sql, args)
        except Exception as e:
            logging.error(e)
            logging.error('%s: %s' % (sql, str(args)))

    def add_nodes(self, node, lon, lat):
        self._execute("INSERT INTO osm_nodes VALUES (?,?,?);", (node, lon, lat))

    def add_ways(self, way):
        self._execute("INSERT INTO osm_ways VALUES (?);", (way,))

    def add_relations(self, relation):
        self._execute("INSERT INTO osm_relations VALUES (?);", (relation,))

    def add_nodes_tags(self, node, k, v):
        self._execute("INSERT INTO osm_nodes_tags VALUES (?,?,?);", (node, k, v))

    def add_ways_tags(self, way, k, v):
        self._execute("INSERT INTO osm_ways_tags VALUES (?,?,?);", (way, k, v))

    def add_relations_tags(self, relation, k, v):
        self._execute("INSERT INTO osm_relations_tags VALUES (?,?,?);", (relation, k, v))

    def add_ways_nds(self, way, nr, ref):
        self._execute("INSERT INTO osm_ways_nds VALUES (?,?,?);", (way, nr, ref))

    def add_relations_members(self, relation, nr, ref, role, el_type):
        self._execute("INSERT INTO osm_relations_members VALUES (?,?,?,?,?);", (relation, nr, ref, role, el_type))


class CsvOutput:
    """Store parsed osm data in csv files for bulk uploads.
    """

    def __init__(self, output_folder, encoding='utf-16LE', delimiter=';'):
        """
        Args:
            output_folder (str): Path to output folder.
            encoding (optional[str]): encoding of csv files.
            delimiter (optional[str]): csv field delimiter char.

        Warning:
            Make sure to clean line breaks, quote chars or delimiters from string data.
            I am not checking those (too many things can go wrong).
            If you don't, your bulk upload may fail.

        """
        self.output_folder = output_folder
        self.delimiter = delimiter
        self.encoding = encoding
        self.osm_nodes = None
        self.osm_ways = None
        self.osm_relations = None
        self.osm_nodes_tags = None
        self.osm_ways_tags = None
        self.osm_relations_tags = None
        self.osm_ways_nds = None
        self.osm_relations_members = None

    def __enter__(self):
        self.osm_nodes = open(os.path.join(self.output_folder, 'osm_nodes.csv'), 'w', encoding=self.encoding)
        self.osm_ways = open(os.path.join(self.output_folder, 'osm_ways.csv'), 'w', encoding=self.encoding)
        self.osm_relations = open(os.path.join(self.output_folder, 'osm_relations.csv'), 'w', encoding=self.encoding)
        self.osm_nodes_tags = open(os.path.join(self.output_folder, 'osm_nodes_tags.csv'), 'w', encoding=self.encoding)
        self.osm_ways_tags = open(os.path.join(self.output_folder, 'osm_ways_tags.csv'), 'w', encoding=self.encoding)
        self.osm_relations_tags = open(os.path.join(self.output_folder, 'osm_relations_tags.csv'), 'w', encoding=self.encoding)
        self.osm_ways_nds = open(os.path.join(self.output_folder, 'osm_ways_nds.csv'), 'w', encoding=self.encoding)
        self.osm_relations_members = open(os.path.join(self.output_folder, 'osm_relations_members.csv'), 'w', encoding=self.encoding)
        return self

    def __exit__(self, type, value, traceback):
        _ = type, value, traceback
        self.osm_nodes.close()
        self.osm_ways.close()
        self.osm_relations.close()
        self.osm_nodes_tags.close()
        self.osm_ways_tags.close()
        self.osm_relations_tags.close()
        self.osm_ways_nds.close()
        self.osm_relations_members.close()

    def add_nodes(self, node, lon, lat):
        self.osm_nodes.write(self.delimiter.join(str(x) for x in (node, lon, lat)) + '\n')

    def add_ways(self, way):
        self.osm_ways.write(self.delimiter.join(str(x) for x in (way,)) + '\n')

    def add_relations(self, relation):
        self.osm_relations.write(self.delimiter.join(str(x) for x in (relation,)) + '\n')

    def add_nodes_tags(self, node, k, v):
        self.osm_nodes_tags.write(self.delimiter.join(str(x) for x in (node, k, v)) + '\n')

    def add_ways_tags(self, way, k, v):
        self.osm_ways_tags.write(self.delimiter.join(str(x) for x in (way, k, v)) + '\n')

    def add_relations_tags(self, relation, k, v):
        self.osm_relations_tags.write(self.delimiter.join(str(x) for x in (relation, k, v)) + '\n')

    def add_ways_nds(self, way, nr, ref):
        self.osm_ways_nds.write(self.delimiter.join(str(x) for x in (way, nr, ref)) + '\n')

    def add_relations_members(self, relation, nr, ref, role, el_type):
        self.osm_relations_members.write(self.delimiter.join(str(x) for x in (relation, nr, ref, role, el_type)) + '\n')


def default_clean_str(s):
    """Clean strings"""
    s = s.replace(';', ':')
    s = s.replace(',', ':')
    s = s.replace('\r', ' ')
    s = s.replace('\n', ' ')
    s = s.replace("'", "")
    s = s.replace('"', '')
    s = s.strip().lower()
    return s


def parse_osm(osm_bz2_file, output_module, clean_str=None):
    """Parse compressed osm (xlm) data (osm.bz2)

    Args:
        osm_bz2_file (str): Path to compressed osm.bz2 data file.
        output_module (object): handler object for parsed data.
        clean_str (optional[function]): function to clean up key and value strings.

    Note:
        It looks complicated, but it's really not. I use ElementTree.iterparse
        beacuse I don't want want to parse the entire data file at once (they can be HUGE),
        but instead iterate through the items and then ``forget`` them once they are parsed

    """
    clean_str = clean_str or (lambda x: x)
    with bz2.BZ2File(osm_bz2_file) as f:
        context = ElementTree.iterparse(f, events=('start', 'end'))
        # finde root tag
        root = None
        for event, element in context:
            if event == 'start' and element.tag == 'osm':
                root = element
                break
        add_tag = output_module.add_nodes_tags  # changeable function
        nr = 0  # position of child node
        for event, element in context:
            if event == 'start':
                if element.tag == 'node':
                    el_id = int(element.attrib['id'])
                    lon = float(element.attrib['lon'])
                    lat = float(element.attrib['lat'])
                    add_tag = output_module.add_nodes_tags
                    output_module.add_nodes(el_id, lon, lat)
                elif element.tag == 'way':
                    el_id = int(element.attrib['id'])
                    nr = 0
                    add_tag = output_module.add_ways_tags
                    output_module.add_ways(el_id)
                elif element.tag == 'relation':
                    el_id = int(element.attrib['id'])
                    nr = 0
                    add_tag = output_module.add_relations_tags
                    output_module.add_relations(el_id)
                elif element.tag == 'tag':
                    k = clean_str(element.attrib['k'])
                    v = clean_str(element.attrib['v'])
                    add_tag(el_id, k, v)
                elif element.tag == 'nd':
                    ref = int(element.attrib['ref'])
                    nr += 1
                    output_module.add_ways_nds(el_id, nr, ref)
                elif element.tag == 'member':
                    role = clean_str(element.attrib['role'])
                    ref = int(element.attrib['ref'])
                    el_type = element.attrib['type']
                    nr += 1
                    output_module.add_relations_members(el_id, nr, ref, role, el_type)
                elif element.tag == 'bounds':
                    pass
                else:
                    logging.warning('Unknown tag: %s' % (element.tag,))
            root.clear()  # IMPORTATNT: clear parsed nodes to no clog memory
    logging.info('FINISHED')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
