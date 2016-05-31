import os.path, re
import lxml.etree as et
from .annotation_transforms import transforms

DIR = os.path.abspath(os.path.dirname(__file__))

src_file = DIR + '/../working_files/dccode-cited.xml'
dst_file = DIR + '/../working_files/dccode-sorted.xml'


def sort_nodes():
    parser = et.XMLParser(remove_blank_text=True)
    print('sorting nodes...')
    with open(src_file) as f:
        dom = et.parse(f, parser)

    session_nodes = dom.xpath('/library/collection/collection')
    for session_node in session_nodes:
    	session_nodes[1:] = sorted(session_node[1:],key=get_normalized_dc_law_num)

    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

dc_law_num_re = re.compile(r'(\d+)-(\d+)(\w*)')
def get_normalized_dc_law_num(law_node):
    law_num = law_node.xpath('string(num)') or '0-0'
    parts = dc_law_num_re.match(law_num).groups()
    return '{0:0>3}-{1:0>4}{2}'.format(*parts)
