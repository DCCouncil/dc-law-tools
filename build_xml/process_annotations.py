#!/usr/bin/env python
"""
process_annotations takes the output from process_annotations.py
and processes all the annotations into computer-readable,
structured data, rather than a bunch of human-readable text.

It runs all the transforms defined in annotation_transforms.

To add a new transform, add it to the list defined in
./annotation_transforms/__init__.py
"""


import os.path
import lxml.etree as et
from .annotation_transforms import transforms

DIR = os.path.abspath(os.path.dirname(__file__))

src_file = DIR + '/../working_files/dccode-no-placeholders.xml'
dst_file = DIR + '/../working_files/dccode-annotated.xml'


def process_annotations():
    parser = et.XMLParser(remove_blank_text=True)
    print('processing annotations...')
    with open(src_file) as f:
        dom = et.parse(f, parser)

    for transform in transforms:
        transform(dom)

    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

if __name__ == '__main__':
    process_annotations()
