"""
split_placeholders takes the output from insert_tables.py
and splits all the range placeholders into individual
placeholders. This cannot be done automatically, so we
use a lookup table (placeholders.json) created by the
Codification Council.

some sections in placeholders.json do not have all split sections
included because raw docs included the later sections (by mistake).
When we get accurate data, will need to re-add those sections.
"""

import os.path, json, re
import lxml.etree as et
from copy import deepcopy

sec_re = re.compile(r'(\d{1,2})-(\d+)\.?(\d*)([a-z]*)')

DIR = os.path.abspath(os.path.dirname(__file__))
src_file = DIR + '/../working_files/dccode-tables.xml'
dst_file = DIR + '/../working_files/dccode-no-placeholders.xml'
placeholders_file = DIR + '/placeholders.json'

def split_placeholders():
    parser = et.XMLParser(remove_blank_text=True)

    print('splitting placeholders')
    with open(placeholders_file) as f:
        placeholders = json.load(f)

    with open(src_file) as f:
        dom = et.parse(f, parser)
    for start_num, placeholder in placeholders.items():
        working_node = orig_node = dom.xpath('//section[string(num)="{}"]'.format(start_num))[0]

        parent_node = orig_node.getparent()
        last_num = orig_node.xpath('string(num-end)')
        if last_num not in placeholder['end']:
            import ipdb
            ipdb.set_trace()
        orig_node.remove(orig_node.find('num-end'))

        for sect_data in placeholder['sections']:
            if sect_data['num'] != start_num and dom.xpath('//section[string(num)="{}"]'.format(sect_data['num'])):
                continue
            new_node = deepcopy(orig_node)
            new_node.find('num').text = sect_data['num']
            new_node.find('heading').text = sect_data['heading']
            if new_node.find('text') is not None:
                new_node.find('text').text = placeholder['text'].format(num=sect_data['num'])
            parent_node.insert(parent_node.index(working_node) + 1, new_node)
        parent_node.remove(orig_node)
    leftovers = dom.xpath('//section[num-end]')
    if leftovers:
        import ipdb
        ipdb.set_trace()

    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))
