#!/usr/bin/env python
"""
The Lexis parser does not parse tables, so this script
inserts manually-created html tables defined in tables.xml.

tables.xml *must be* updated when a new version of the code
comes out.
"""
import os.path
import sys, lxml.etree as etree, re

DIR = os.path.abspath(os.path.dirname(__file__))


num_re = re.compile('<num>(?P<num>.+?)</num>')
table_re = re.compile(r'@@TABLE@@')

def insert_tables():
    xml_path = DIR + '/../working_files/dccode.xml'
    tables_path = DIR + '/tables.xml'
    out_path = DIR + '/../working_files/dccode-tables.xml'

    with open(xml_path) as f:
        xml = f.read() # etree.parse(f).getroot()

    with open(tables_path) as f:
        Tables = etree.parse(f).getroot()

    sections = xml.split('<section>\n')

    print('inserting tables...')
    out = []
    for section in sections:
        try:
            num = num_re.search(section).group(1)
        except:
            import ipdb
            ipdb.set_trace()
        section_tables = Tables.find('section[@id="{}"]'.format(num))
        if section_tables is not None:
            tables = section_tables.getchildren()
            i = 0
            def replacement(match):
                nonlocal i
                table = tables[i]
                out = etree.tostring(table, pretty_print=True, encoding='utf-8').decode('utf-8')
                table.set('inserted', 'true')
                i = i + 1
                return out
            out.append(table_re.sub(replacement, section))
        else:
            out.append(section)

    if len(Tables.findall('section/table[@inserted]')) != len(Tables.findall('section/table')):
        import ipdb
        ipdb.set_trace()
        raise Exception('some tables not inserted')

    out = '<section>\n'.join(out).encode('utf-8')
    dom = etree.fromstring(out)

    with open(out_path, 'wb') as f:
        f.write(etree.tostring(dom, pretty_print=True, encoding="utf-8"))

if __name__ == '__main__':
    insert_tables()
