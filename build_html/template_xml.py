#!/usr/bin/env python
"""
template the xml using xslt 
"""
from .preprocessors.utils import xcache, update_cache
from copy import deepcopy
import os, lxml.etree as et
import json

DIR = os.path.abspath(os.path.dirname(__file__))


xslt_dir = os.path.join(DIR, 'preprocessors', 'templates')
bld_file = os.path.join(DIR, '../working_files/dccode-html-bld.xml')
out_dir = os.path.join(DIR, '../../dc-law-html')
index_file = os.path.join(out_dir, 'index.bulk')

generators = (
    (
        '/library',
        ('.', './/collection'),
        'library.xslt',
        {'cloneRootCache': True, 'index': False},
    ),
    (
        '//document[@id="D.C. Code"][1]',
        ('.', './/container[not(cache/noPage)]', './/section'),
        'code.xslt',
        {'cloneRootCache': True},
    ),
    (
        '//document[starts-with(@id, "D.C. Law")]',
        ('.',),
        'dclaw.xslt',
        {'index': False},
    ),
)

def template_xml():
    print('templating...')
    with open(bld_file) as f:
        dom = et.parse(f)

    with open(index_file, 'w') as _index:
        def index(url, node, xhtml):
            instruction = {'index': {'_index': 'dc', '_type': 'page', '_id': url}}
            body_node = (xhtml.xpath('//div[@class="toc"][*] | //div[@class="content"]') or [None])[0]
            doc = {
                'url': url,
                'title': node.xpath('string(cache/title)'),
                'body': get_text(body_node),
                'num': node.xpath('string(num)'),
            }
            _index.write(json.dumps(instruction) + '\n')
            _index.write(json.dumps(doc) + '\n')

        for root_xpath, node_xpaths, xslt_fn, opts in generators:
            roots = dom.xpath(root_xpath)
            with open(os.path.join(xslt_dir, xslt_fn), 'r') as f:
                template = et.XSLT(et.parse(f))
            for root in roots:
                cloneRootCache = opts.get('cloneRootCache', False)
                if cloneRootCache:
                    root_cache = deepcopy(root.find('cache'))
                    root_cache.tag = 'root'
                for node_xpath in node_xpaths:
                    nodes = root.xpath(node_xpath)
                    # import ipdb
                    # ipdb.set_trace()
                    for node in nodes:
                        if cloneRootCache:
                            update_cache(node, root_cache)
                        url = xcache(node, 'url')
                        if url.endswith('/'):
                            url += 'index.html'
                        url_dir = os.path.dirname(url)
                        xhtml = template(node)
                        if opts.get('index', True):
                            index(url, node, xhtml)
                        try:
                            os.makedirs(out_dir + url_dir)
                        except:
                            pass
                        with open(out_dir + url, 'wb') as f:
                            xhtml.write(f, encoding='utf-8', pretty_print=True)

def get_text(node):
    if node is None:
        return ''
    text = (node.text or '').strip() + ' '
    for child in node.iterchildren():
        text += get_text(child)
    text += (node.tail or '').strip() + ' '
    return text
