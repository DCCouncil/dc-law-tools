#!/usr/bin/env python
"""
merge all the xml documents into one ginormous xml file
for ease of processing.
"""
import os, lxml.etree as et

DIR = os.path.abspath(os.path.dirname(__file__))

src_dir = os.path.join(DIR, '../../dc-law-xml')
bld_file = os.path.join(DIR, '../working_files/dccode-html-bld.xml')


def merge_xml():
    print('merging...')
    parser = et.XMLParser(remove_blank_text=True)

    fn = os.path.join(src_dir, 'index.xml')

    with open(fn) as f:
        dom = et.parse(f, parser)

    dom.xinclude()

    with open(bld_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))
