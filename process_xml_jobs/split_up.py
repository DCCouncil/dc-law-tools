#!/usr/bin/env python
"""
Split the single file dccode into multiple files:

  * /index.xml with refs to each title
  * /Title-*.xml, one for each title with links to each section
  * /sections/*.xml, one for each section
"""

import os, lxml.etree as et
import os.path
from tqdm import tqdm

DIR = os.path.abspath(os.path.dirname(__file__))

src_file = DIR + '/../working_files/dccode-annotated.xml'
dst_dir = DIR + '/../../dc-law-xml'

parser = et.XMLParser(remove_blank_text=True)
with open(src_file) as f:
    dom = et.parse(f, parser)

def ensure_dst_dirs(path):
    try:
        os.makedirs(os.path.join(dst_dir, path))
    except:
        pass
    
ensure_dst_dirs('code/sections')
ensure_dst_dirs('statutes/statutes')

def split_and_link_node(node, base_dir='', rel_prefix='', write_to_disk=True):
    file_name = node.xpath('string(num)') or node.xpath('string(section)') or node.xpath('string(section-start)') or node.xpath('string(lawNum)') or 'index'
    rel_path = os.path.join('.', rel_prefix + file_name + '.xml')
    if write_to_disk:
        with open(os.path.join(dst_dir, base_dir, rel_path), 'wb') as f:
            f.write(et.tostring(node, pretty_print=True, encoding="utf-8"))
    xi = et.Element("{http://www.w3.org/2001/XInclude}include")
    xi.set("href", rel_path)
    node.addprevious(xi)
    node.getparent().remove(node)

def split_up():
    print('splitting up...')
    sections = dom.xpath('//section[parent::container]|//placeholder')
    
    print('writing sections...')
    for section in tqdm(sections):
        split_and_link_node(section, 'code', 'sections/', write_to_disk=False)

    print('writing titles...')
    titles = dom.xpath('//container[../@childPrefix = "Title"]')
    for title in tqdm(titles):
        split_and_link_node(title, 'code', 'Title-')

    codes = dom.xpath('//code')
    for code in codes:
        split_and_link_node(code, '', 'code/')

    print('writing statutes...')
    statutes = dom.xpath('//statute')
    for statute in tqdm(statutes):
        split_and_link_node(statute, 'statutes', 'statutes/')

    statuteses = dom.xpath('//statutes')
    for statutes in statuteses:
        split_and_link_node(statutes, '', 'statutes/')

    with open(os.path.join(dst_dir, 'index.xml'), 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

if __name__ == '__main__':
    split_up()
