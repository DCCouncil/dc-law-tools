"""
Each section contains a `History` annotation that, in
parantheses, lists each statute that has changed the section.
Each statute should (but might not always) 

This script first transforms the dom such that:

    <code>...</code>

becomes:

    <law>
      <code>...</code>
      <statutes>
        <dc>
          <permanent />
          <temporary />
          <emergency />
        </dc>
        <fed />
      </statutes>
    </law>

Then it creates a new <statute> entry for each DC statute that it finds in the history:

    <law><statutes><dc><permanent>
      <statute stub="true">
        <date>DD-MM-YYYY</date>
        <lawNum>XX-XXX</lawNum>
        <billNum>YY-YYY</billNum>
      </statute>
    </permanent></dc></statutes></law>

and a new <statute> entry for each federal law:
TODO: figure out federal statute structure...

    <law><statutes><fed>
      <statute stub="true">
        ???
      </statute>
    </fed></statutes></law>

"""
import lxml.etree as et
import re

dc_law_re = re.compile(r"D\.?\s*C\.?\s+Law\s+(\d+)\s?[-–]+\s?(\d+\w?)")

def make_statutes(dom):
    root = dom.getroot()

    code_node = _make_node('code', root, root.getchildren(), **root.attrib)
    root.tag = 'law'
    for k in root.attrib.keys():
      del root.attrib[k]

    statutes_node = _make_node('statutes', root)
    dc_statutes_node = _make_node('dc', statutes_node)

    code_string = et.tostring(dom).decode()

    dc_law_cite_nums = dc_law_re.findall(code_string)

    dc_law_cites = ['-'.join(x) for x in dc_law_cite_nums]

    dc_law_cites = set(dc_law_cites)

    for cite in dc_law_cites:
        statute_node = _make_node('statute', dc_statutes_node, stub=True)
        law_num_node = _make_node('lawNum', statute_node, text=cite)

attr_lookup = {True: 'true', False: 'false'}

def _make_node(tag, parent=None, children=[], text='', **attributes):
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
