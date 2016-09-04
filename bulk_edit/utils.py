"""
Split the single file dccode into multiple files:

  * /index.xml with refs to each title
  * /Title-*.xml, one for each title with links to each section
  * /sections/*.xml, one for each section
"""

import os, lxml.etree as et
import os.path, re
import contextlib, glob

DIR = os.path.abspath(os.path.dirname(__file__))
src_file = DIR + '/../working_files/dccode-cited.xml'
dst_dir = DIR + '/../../dc-law-xml'

parser = et.XMLParser(remove_blank_text=True)

def work_on_files(repo_path, glob_path):
    file_paths = glob.glob(os.path.join(repo_path, glob_path))
    for file_path in file_paths:
        with open(file_path) as f:
            dom = et.parse(f, parser)
            yield dom
        with open(file_path, 'wb') as f:
            f.write(et.tostring(dom, pretty_print=True, encoding="utf-8", xml_declaration=True))

def _ensure_dst_dirs(dst_dir, *path):
    try:
        os.makedirs(os.path.join(dst_dir, *path))
    except:
        pass

def _split_and_link_node(node, dst_dir, base_path, rel_path):
    abs_path = os.path.join(dst_dir, *(base_path + rel_path))
    try:
        with open(abs_path, 'wb') as f:
            f.write(et.tostring(node, pretty_print=True, encoding="utf-8", xml_declaration=True))
    except IOError:
        _ensure_dst_dirs(dst_dir, os.path.dirname(abs_path))
        with open(abs_path, 'wb') as f:
            f.write(et.tostring(node, pretty_print=True, encoding="utf-8", xml_declaration=True))

    xi = et.Element("{http://www.w3.org/2001/XInclude}include")
    xi.set("href", os.path.join('.', *rel_path))
    node.getparent().replace(node, xi)
    import ipdb
    ipdb.set_trace()

def _split_and_link_nodes(base_node, dst_dir, base_path, xpath, rel_path_pattern, child_splits=[]):
    nodes = base_node.xpath(xpath)
    for node in nodes:
        num = (node.xpath('num[1]/text()') or [''])[0]
        rel_path = [x.format(num=num) if type(x) == str else x(node, num) for x in rel_path_pattern]
        for child_split in child_splits:
            child_base_path = base_path + rel_path[:-1]
            _split_and_link_nodes(node, dst_dir, child_base_path, *child_split)

        _split_and_link_node(node, dst_dir, base_path, rel_path)


sec_splitter_re = re.compile(r'[-:]')
get_sec_fn = lambda node, num: sec_splitter_re.split(num, 1)[1] + '.xml'
get_perm_law_fn = lambda node, num: num.split('-')[1] + '.xml'
get_period = lambda node, num: node.get('name').split(' ')[-1]

_default_node_splits = (
    ('//document[@id="D.C. Code"]', ('dc', 'council', 'code', 'index.xml'),(
        ('.//container[@childPrefix = "Title"]/container', ('titles', '{num}', 'index.xml'), (
            ('.//section', ('sections', get_sec_fn,)),
         )),
    )),
    ('//collection[@name="dclaws"]/collection', ('dc', 'council', 'periods', get_period, 'laws', 'index.xml'), (
        ('document', (get_perm_law_fn,)),
    )),
)

def remove_xml_base_attrib(dom):
    base_nodes = dom.xpath('//*[@xml:base]')
    for base_node in base_nodes:
        del base_node.attrib['{http://www.w3.org/XML/1998/namespace}base']
    return dom

def split_up(dom, dst_dir, node_splits=_default_node_splits):
    dom = remove_xml_base_attrib(dom)

    for node_split in node_splits:
        _split_and_link_nodes(dom, dst_dir, [''], *node_split)

    with open(os.path.join(dst_dir, 'index.xml'), 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))


def merge_xml(src_dir):
    fn = os.path.join(src_dir, 'index.xml')
    with open(fn) as f:
        dom = et.parse(f, parser)
    dom.xinclude()
    return dom

@contextlib.contextmanager
def work_on_dom(repo_path, interactive=False):
    dom = merge_xml(repo_path)
    yield dom
    if interactive:
        import ipdb
        ipdb.set_trace()
    else:
        split_up(dom, repo_path)

