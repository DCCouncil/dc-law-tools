#!/usr/bin/env python
"""
template the xml using xslt 
"""
import moment, os, lxml.etree as et

DIR = os.path.abspath(os.path.dirname(__file__))


xslt_file = os.path.join(DIR, './dc-law.xslt')
bld_file = os.path.join(DIR, '../working_files/dccode-html-bld.xml')
out_dir = os.path.join(DIR, '../../dc-law-html')

def template_xml():
    with open(bld_file) as f:
        dom = et.parse(f)
    # import ipdb
    # ipdb.set_trace()
    with open(xslt_file, 'r') as f:
        template = et.XSLT(et.parse(f))
        xhtml = template(dom, genpath='/laws[1]/code[1]')

    with open(os.path.join(out_dir, 'index.html'), 'wb') as f:
        xhtml.write(f, encoding='utf-8', pretty_print=True)


if __name__ == '__main__':
    template_xml()
