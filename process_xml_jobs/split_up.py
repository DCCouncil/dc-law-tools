#!/usr/bin/env python
"""
Split the single file dccode into multiple files:

  * /index.xml with refs to each title
  * /Title-*.xml, one for each title with links to each section
  * /sections/*.xml, one for each section
"""

import os, lxml.etree as et
import os.path

DIR = os.path.abspath(os.path.dirname(__file__))

src_file = DIR + '/../working_files/dccode-annotated.xml'
dst_dir = DIR + '../../../dc-law-xml'

parser = et.XMLParser(remove_blank_text=True)
with open(src_file) as f:
    dom = et.parse(f, parser)

try:
    os.makedirs(dst_dir + '/code/sections')
except:
    pass

def process(node, fn_dir='/'):
    num = node.xpath('string(num)') or node.xpath('string(section)') or node.xpath('string(section-start)')
    fn = fn_dir + num + '.xml'
    with open(dst_dir + '/code' + fn, 'wb') as f:
        f.write(et.tostring(node, pretty_print=True, encoding="utf-8"))
    xi = et.Element("{http://www.w3.org/2001/XInclude}include")
    xi.set("href", '.' + fn)
    node.addprevious(xi)
    node.getparent().remove(node)

def split_up():
    print('splitting up...')
    sections = dom.xpath('//section[parent::container]|//placeholder')
    for section in sections:
        process(section, '/sections/')

    titles = dom.xpath('//container[prefix/text()="Title"]')
    for title in titles:
        process(title, '/Title-')

    with open(dst_dir + '/code/index.xml', 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

if __name__ == '__main__':
    split_up()
