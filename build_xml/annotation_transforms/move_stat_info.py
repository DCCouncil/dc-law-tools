"""
Move legislative history, construction, expiration of law nodes into the proper statute stub node.

    ...
    <statute stub="true">
      ...
      <history>
        <narrative>
          {text of legislative history node}
        </narrative>
      </history>
      <construction>
        {text of construction}
      </construction>
    </statute>
"""

import lxml.etree as et
import re
law_num_re = re.compile(r'\d+-\d+\w?')

def move_stat_info(dom):
    print('  moving statute data')
    leg_hist_nodes = dom.xpath('//annoGroup[heading/text()="Legislative History"]')
    dc_law_parent_node = dom.find('//document[@id="D.C. Law 3-171"]/../..')
    if dc_law_parent_node is None:
        import ipdb
        ipdb.set_trace()

    for leg_node in leg_hist_nodes:
        if leg_node.xpath('count(text)') < 2:
            print('BAD NODE COUNT', et.tostring(leg_node))
            continue
        leg_heading = leg_node.xpath('text[1]/text()')[0]
        if leg_heading == 'Legislative history of Law 20':
            leg_heading = 'Legislative history of Law 20-110'
        law_num = law_num_re.search(leg_heading)
        if law_num is None:
            print('BAD LEG HEADING', et.tostring(leg_node))
            continue
        law_num = law_num.group()
        law_node = dc_law_parent_node.find('*/document[@id="D.C. Law {}"]'.format(law_num))
        leg_node.getparent().remove(leg_node)
        if law_node is None:
            law_node = make_statute(dc_law_parent_node, law_num)
        elif law_node.find('history'):
            continue
        if leg_node.xpath('text[2]/text()')[0].lower().startswith('see note'):
            print('Missing:', law_num)
            law_node.set('flag', 'true')
        narrative_nodes = leg_node.xpath('text[position()>1]')
        for narrative_node in narrative_nodes:
            narrative_node.tag = 'narrative'
        hist_node = _make_node('history', law_node, children=narrative_nodes)


law_num_split_re = re.compile(r'[-:]')
def make_statute(dc_law_parent_node, law_num):
    law_parts = law_num_split_re.split(law_num, 1)
    parent_node = dc_law_parent_node.find('collection[@name="Council Session {}"]'.format(law_parts[0]))
    if parent_node is None:
        import ipdb
        ipdb.set_trace()
    law_node = _make_node('document', parent_node, id = 'D.C. Law {}'.format(law_num), flag='true')
    _make_node('num', law_node, law_num, type='law')
    cite_node = _make_node('cites', law_node)
    _make_node('law', cite_node, session=law_parts[0], lawId=law_parts[1])
    return law_node

attr_lookup = {True: 'true', False: 'false'}
def _make_node(tag, parent=None, text='', children=[], **attributes):
    node = et.Element(tag)
    if parent is not None:
        parent.append(node)
    for child in children:
        node.append(child)
    for k, v in attributes.items():
        node.attrib[k] = attr_lookup.get(v, v)
    if text:
      node.text = text
    return node
