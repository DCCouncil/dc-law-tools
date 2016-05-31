"""
Split the single file dccode into multiple files:

  * /index.xml with refs to each title
  * /Title-*.xml, one for each title with links to each section
  * /sections/*.xml, one for each section
"""

import os, lxml.etree as et
import os.path, re
import click

DIR = os.path.abspath(os.path.dirname(__file__))
src_file = DIR + '/../working_files/dccode-cited.xml'
dst_dir = DIR + '/../../dc-law-xml'

def ensure_dst_dirs(*path):
    try:
        os.makedirs(os.path.join(dst_dir, *path))
    except:
        pass

def split_and_link_node(node, base_path, rel_path):
    abs_path = os.path.join(dst_dir, *(base_path + rel_path))
    try:
        with open(abs_path, 'wb') as f:
            f.write(et.tostring(node, pretty_print=True, encoding="utf-8"))
    except IOError:
        ensure_dst_dirs(os.path.dirname(abs_path))
        with open(abs_path, 'wb') as f:
            f.write(et.tostring(node, pretty_print=True, encoding="utf-8"))

    xi = et.Element("{http://www.w3.org/2001/XInclude}include")
    xi.set("href", os.path.join(*rel_path))
    try:
        node.getparent().replace(node, xi)
    except:
        import ipdb
        ipdb.set_trace()

def split_and_link_nodes(base_node, base_path, xpath, rel_path_pattern, child_splits=[]):
    nodes = base_node.xpath(xpath)
    for node in nodes:
        num = (node.xpath('num[1]/text()') or [''])[0]
        rel_path = [x.format(num=num) if type(x) == str else x(node, num) for x in rel_path_pattern]
        for child_split in child_splits:
            child_base_path = base_path + rel_path[:-1]
            split_and_link_nodes(node, child_base_path, *child_split)

        split_and_link_node(node, base_path, rel_path)


sec_splitter_re = re.compile(r'[-:]')
get_sec_fn = lambda node, num: sec_splitter_re.split(num, 1)[1] + '.xml'
get_perm_law_fn = lambda node, num: num.split('-')[1] + '.xml'
get_session = lambda node, num: node.get('name').split(' ')[-1]

node_splits = (
    ('//document[@id="D.C. Code"]', ('dc', 'council', 'code', 'index.xml'),(
        ('.//container[@childPrefix = "Title"]/container', ('titles', '{num}', 'index.xml'), (
            ('.//section', ('sections', get_sec_fn,)),
         )),
    )),
    ('//collection[@name="dclaws"]/collection', ('dc', 'council', 'sessions', get_session, 'laws', 'index.xml'), (
        ('document', (get_perm_law_fn,)),
    )),
)


def split_up():
    print('splitting up...')
    parser = et.XMLParser(remove_blank_text=True)
    with open(src_file) as f:
        dom = et.parse(f, parser)
    for node_split in node_splits:
        split_and_link_nodes(dom, [''], *node_split)

    with open(os.path.join(dst_dir, 'index.xml'), 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

