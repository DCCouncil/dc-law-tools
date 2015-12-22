"""
Each section contains a `History` annotation that, in
parantheses, lists each statute that has changed the section.
Each statute should (but might not always) 

This script first transforms the dom such that:

    <law>
      <code>...</code>
    </law>

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
    statutes_node = et.Element('statutes')
    dom.getroot().append(statutes_node)
    dc_statutes_node = et.Element('dc')
    statutes_node.append(dc_statutes_node)

    code_string = et.tostring(dom).decode()


    dc_law_cite_nums = dc_law_re.findall(code_string)

    dc_law_cites = ['-'.join(x) for x in dc_law_cite_nums]

    dc_law_cites = set(dc_law_cites)

    for cite in dc_law_cites:
        statute_node = et.Element('statute')
        dc_statutes_node.append(statute_node)
        statute_node.attrib['stub'] = 'true'
        law_num_node = et.Element('lawNum')
        statute_node.append(law_num_node)
        law_num_node.text = cite
