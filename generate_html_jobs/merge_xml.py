#!/usr/bin/env python
"""
merge all the xml documents into one ginormous xml file
for ease of processing.
"""
import os, lxml.etree as et

DIR = os.path.abspath(os.path.dirname(__file__))

src_dir = os.path.join(DIR, '../../dc-law-xml')
bld_file = os.path.join(DIR, '../working_files/dccode-html-bld.xml')

parser = et.XMLParser(remove_blank_text=True)

def merge_xml():
    fn = os.path.join(src_dir, 'index.xml')
    dom = load_child_dom(fn)

    with open(bld_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

def load_child_dom(file_path):
    with open(file_path) as f:
        dom = et.parse(f, parser)

    parent_dir = os.path.dirname(file_path)
    xincludes = dom.findall('//{http://www.w3.org/2001/XInclude}include')
    
    for xi in xincludes:
        rel_path = xi.attrib['href']
        child_path = os.path.join(parent_dir, rel_path)
        child_dom = load_child_dom(child_path).getroot()
        xi.addprevious(child_dom)
        xi.getparent().remove(xi)

    return dom

if __name__ == '__main__':
    merge_xml()
