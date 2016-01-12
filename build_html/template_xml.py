#!/usr/bin/env python
"""
template the xml using xslt 
"""
import os, lxml.etree as et
from tqdm import tqdm

DIR = os.path.abspath(os.path.dirname(__file__))


xslt_file = os.path.join(DIR, './dc-law.xslt')
bld_file = os.path.join(DIR, '../working_files/dccode-html-bld.xml')
out_dir = os.path.join(DIR, '../../dc-law-html')

def template_xml():
    with open(bld_file) as f:
        dom = et.parse(f)
    # dom.xinclude()
    with open(xslt_file, 'r') as f:
        template = et.XSLT(et.parse(f))

    nodes = dom.xpath('//code | //section[num] | //container[not(../@childPrefix = "Division" or ../@childPrefix = "Subtitle")]')

    for node in tqdm(nodes):
        url = gen_url(node)
        url_dir = os.path.dirname(url)

        genpath = dom.getpath(node)
        xhtml = template(dom, genpath=genpath)
        try:
            os.makedirs(os.path.join(out_dir, url_dir))
        except:
            pass
        with open(os.path.join(out_dir, url), 'wb') as f:
            xhtml.write(f, encoding='utf-8', pretty_print=True)

def gen_url(node):
    if node.tag == 'section':
        return os.path.join('sections', node.xpath('num/text()')[0] + '.html')
    elif node.tag == 'code':
        return 'index.html'
    else:
        ancestors = node.xpath('ancestor-or-self::container[not(../@childPrefix = "Division" or ../@childPrefix = "Subtitle")]')
        out = ''
        for ancestor in ancestors:
            out += ancestor.xpath('../@childPrefix')[0] + '-' + ancestor.xpath('num/text()')[0] + '/'
        out += 'index.html'
        return out

if __name__ == '__main__':
    template_xml()
