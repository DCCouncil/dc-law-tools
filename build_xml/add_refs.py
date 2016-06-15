import click
import os, json, re
import lxml.etree as et

DIR = os.path.abspath(os.path.dirname(__file__))
src_file = DIR + '/../working_files/dccode-annotated.xml'
dst_file = DIR + '/../working_files/dccode-cited.xml'

pdf_path = DIR + '/../../dc-law-docs-laws/{period}-{lawId}.pdf'

code_cite = r'\d+-\d+(?::\d)?\w*(?:\.\d+\w*)?'

def add_cite_elements(match_object):
    'Function to subsitiue cite elements into cite lists from the regex'
    # group0 should contain the entire list matched by the cite list
    # matcher (can be only 1 citation)
    in_str = match_object.group(0)
    # because we matched the list carefully we can assume any citation of
    # standard DC format is correct.
    return re.sub(r'(' + code_cite + ')', '<cite abs="\\1">\\1</cite>', in_str)


subs = (
    (re.compile(r'(D.C. Law \d+-\w+)'), '<cite doc="\\1">\\1</cite>'),
    (re.compile(r'(§§\s+(?:\d+-\d+(?::\d)?\w*(?:\.\d+\w*)?(?:\(\w+\))*(?:through|\s|,)+)*(?:and)?\s?)(\d+-\d+(?::\d)?\w*(?:\.\d+\w*)?)'), add_cite_elements),
    (re.compile(r'§\s('+code_cite+')'), '§ <cite abs="\\1">\\1</cite>')
)



def add_refs():
    parser = et.XMLParser(remove_blank_text=True)

    print('adding cites')
    with open(src_file) as f:
        dom = et.parse(f, parser)

    code_node = dom.find('//document[@id="D.C. Code"]')
    nodes = code_node.xpath('//annoGroup[not(heading/text()="History")]/annotation') + code_node.xpath('//text')

    with click.progressbar(nodes) as progress_nodes:

        for node in progress_nodes:
            node_text = et.tostring(node, encoding='utf-8').decode()
            count = 0

            # this is overly conservative, but better safe than sorry
            if '1981 Ed.' in node_text or '1973 Ed.' in node_text or 'Home Rule Act' in node_text:
                continue
            for regex, substr in subs:
                node_text, local_count = regex.subn(substr, node_text)
                count += local_count

            if count:
                node.getparent().replace(node, et.fromstring(node_text))

    print('adding pdfs')

    nodes = dom.xpath('//document[starts-with(@id, "D.C. Law")]/cites/law[not(@url)]')
    with click.progressbar(nodes) as progress_nodes:
        for node in progress_nodes:
            if os.path.isfile(pdf_path.format(**node.attrib)):
                node.set('url', './docs/{period}-{lawId}.pdf'.format(**node.attrib))

    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))
