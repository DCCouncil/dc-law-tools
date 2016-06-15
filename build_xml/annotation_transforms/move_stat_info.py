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
from .process_history import get_statute, make_statute, _make_node
import lxml.etree as et
import re
law_num_re = re.compile(r'\d+-\d+\w?')
law_num_split_re = re.compile(r'[-:]')
def move_stat_info(dom):
    reffed_missing = {}
    print('  moving statute data')
    leg_hist_nodes = dom.xpath('//annoGroup[heading/text()="Legislative History"]')
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
        law_node = get_statute(dom, law_num)
        leg_node.getparent().remove(leg_node)
        if law_node is None:
            law_parts = law_num_split_re.split(law_num, 1)
            law_node = make_statute(dom, {'lawNum': law_num, 'dcLaw': {'period':law_parts[0], 'lawId': law_parts[1]}})
        elif law_node.find('history/narrative') is not None:
            continue
        if not leg_node.xpath('text[2]/text()')[0].lower().startswith('law'):
            reffed_missing[law_num] = True
            law_node.set('flag', 'true')
            continue
        reffed_missing.pop(law_num, None)
        hist_node = law_node.find('history')
        if hist_node is None:
            hist_node = _make_node('history', law_node)
        narrative_nodes = leg_node.xpath('text[position()>1]')
        for narrative_node in narrative_nodes:
            narrative_node.tag = 'narrative'
            hist_node.append(narrative_node)
    print('    missing law nums', reffed_missing.keys())

    period_nodes = dom.xpath('/library/collection/collection')
    for period_node in period_nodes:
        period_nodes[1:] = sorted(period_node[1:],key=get_normalized_dc_law_num)
    
dc_law_num_re = re.compile(r'(\d+)-(\d+)(\w*)')
def get_normalized_dc_law_num(law_node):
    law_num = law_node.xpath('string(num)') or '0-0'
    parts = dc_law_num_re.match(law_num).groups()
    return '{0:0>3}-{1:0>4}{2}'.format(*parts)
