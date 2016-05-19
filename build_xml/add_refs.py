import click
import os.path, json, re
import lxml.etree as et

DIR = os.path.abspath(os.path.dirname(__file__))
src_file = DIR + '/../working_files/dccode-annotated.xml'
dst_file = DIR + '/../working_files/dccode-cited.xml'

pdf_path = DIR + '/../../dc-law-xml/laws/permanent/sessions/{session}/{lawId}.pdf'

code_cite = r'\d+-\d+(?::\d)?\w*(?:\.\d+\w*)?'
subs = (
    (re.compile(r'(D.C. Law \d+-\w+)'), '<cite doc="\\1">\\1</cite>'),
    (re.compile(r'&#167;&#167;\s('+code_cite+r',\s)*and\s('+code_cite+')'), lambda match: ', '.join(['<cite doc="{0}">{0}</cite>'.format(x) for x in match.group(1).strip(', ').split(', ')]) + ', and <cite doc="{0}">{0}</cite>'.format(match.group(2))),
    (re.compile(r'&#167;&#167;\s(\d+-\d+(?::\d)?\w*(?:\.\d+\w*)?)(\s?[\w]*\s)(\d+-\d+(?::\d)?\w*(?:\.\d+\w*)?)'), '§§ <cite abs="\\1">\\1</cite>\\2<cite abs="\\3">\\3</cite>'),
    (re.compile(r'&#167;\s('+code_cite+')'), '<cite abs="\\1">§ \\1</cite>'),
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
            node_text = et.tostring(node).decode()
            count = 0

            if '1981 Ed.' in node_text or '1973 Ed.' in node_text:
                continue
            for regex, substr in subs:
                node_text, local_count = regex.subn(substr, node_text)
                count += local_count

            if count:
                node.getparent().replace(node, et.fromstring(node_text))

    print('adding pdfs')

    nodes = dom.xpath('//collection[@name="permanent"]/collection/document/cites/law[not(@url)]')

    with click.progressbar(nodes) as progress_nodes:
        for node in progress_nodes:
            if os.path.isfile(pdf_path.format(**node.attrib)):
                node.set('url', './{lawId}.pdf'.format(**node.attrib))

    import ipdb
    ipdb.set_trace()
    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))
