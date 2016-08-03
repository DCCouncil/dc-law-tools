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
old_code_file = DIR + '/../working_files/2016-03.xml'
src_file = DIR + '/../working_files/dccode-tables.xml'
dst_file = DIR + '/../working_files/dccode-no-placeholders.xml'
library_file = os.path.join(DIR, 'library.xml')
placeholders_file = DIR + '/placeholders.json'

def replace_node(node, new_nodes):
    insert_after_node(node, new_nodes)
    parent = node.getparent()
    parent.remove(node)

def insert_after_node(node, new_nodes):
    parent = node.getparent()
    for i, e in enumerate(new_nodes):
        parent.insert(parent.index(node) + 1 + i, e)

def split_placeholders():
    parser = et.XMLParser(remove_blank_text=True)

    print('splitting placeholders')
    with open(placeholders_file) as f:
        placeholders = json.load(f)

    with open(library_file) as f:
        dom = et.parse(f, parser)

    with open(src_file) as f:
        code_node = et.parse(f, parser).getroot()
        code_node.tag = 'document'
        code_node.set('id', 'D.C. Code')
        old_code_node = dom.find('//document[@id="D.C. Code"]')
        old_code_node.getparent().replace(old_code_node, code_node)

    xml_inserts = placeholders.pop('xml')
    for xml_insert in xml_inserts:
        action = xml_insert['action']
        try:
            node = dom.xpath(xml_insert['xpath'])[0]
        except:
            raise Exception('invalid xpath: {}'.format(xml_insert['xpath']))
        new_nodes = et.XML('<div>' + xml_insert['xml'] + '</div>').getchildren()
        if action == 'insert-after':
            insert_after_node(node, new_nodes)
        elif action == 'replace':
            replace_node(node, new_nodes)


    section_nodes = {node.xpath('string(num)'): node for node in dom.xpath('//section')}
    for start_num, placeholder in placeholders.items():
        try:
            working_node = orig_node = section_nodes[start_num]
        except KeyError:
            print('no start node: {}'.format(start_num))
            continue
            raise Exception('no start node: {}'.format(start_num))

        parent_node = orig_node.getparent()
        last_num = orig_node.xpath('string(num-end)')
        if last_num not in placeholder['end']:
            import ipdb
            ipdb.set_trace()
        orig_node.remove(orig_node.find('num-end'))

        for sect_data in placeholder['sections']:
            if sect_data['num'] != start_num and sect_data['num'] in section_nodes:
                continue
            new_node = deepcopy(orig_node)
            new_node.find('num').text = sect_data['num']
            new_node.find('heading').text = sect_data['heading']
            if new_node.find('text') is not None:
                new_node.find('text').text = placeholder['text'].format(num=sect_data['num'])
            parent_node.insert(parent_node.index(working_node) + 1, new_node)
        parent_node.remove(orig_node)
    leftovers = dom.xpath('//section[num-end]')

    with open(old_code_file) as f:
        old_code = et.parse(f, parser)
    old_sections = old_code.xpath('//section')
    old_section_nodes = {node.xpath('string(num)'): node for node in old_code.xpath('//section')}

    for leftover in leftovers:
        start, end = [leftover.xpath('string(num)'),leftover.xpath('string(num-end)')]
        try:
            start_node = old_section_nodes[start]
        except:
            raise(Exception('invalid start node: {}'.format(start)))
            continue
        try:
            end_node = old_section_nodes[end]
        except:
            raise(Exception('invalid end node: {}'.format(end)))
            continue
        new_nodes = old_sections[old_sections.index(start_node):old_sections.index(end_node)+1]
        if leftover.getparent() is None:
            import ipdb
            ipdb.set_trace()
        replace_node(leftover, new_nodes)

    leftovers = dom.xpath('//section[num-end]')
    if leftovers:
        import ipdb
        ipdb.set_trace()

    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))
