"""
The Lexis parser does not parse tables, so this script
inserts manually-created html tables defined in tables.xml.

tables.xml *must be* updated when a new version of the code
comes out.
"""
import os.path
import lxml.etree as etree, re

DIR = os.path.abspath(os.path.dirname(__file__))
src_file = DIR + '/../working_files/dccode-t1-ch15.xml'
tables_path = DIR + '/tables.xml'
dst_file = DIR + '/../working_files/dccode-tables.xml'


num_re = re.compile('<num>(?P<num>.+?)</num>')
table_re = re.compile(r'@@TABLE@@')
pict_re = re.compile(r'@@PICT@@')
def insert_tables():

    with open(src_file) as f:
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
                if i >=len(tables):
                    import ipdb
                    ipdb.set_trace()
                table = tables[i]
                if table.getchildren():
                    out = etree.tostring(table, pretty_print=True, encoding='utf-8').decode('utf-8')
                else:
                    out = ''
                table.set('inserted', 'true')
                i = i + 1
                return out
            section = table_re.sub(replacement, section)
        elif '@@TABLE@@' in section:
            print('missing tables for section', num)

        # special case: picture converted to table
        if num == '16-916.01':
            table = Tables.find('section[@id="16-916.01"]/table'.format(num))
            table.set('inserted', 'true')
            table_str = etree.tostring(table, pretty_print=True, encoding='utf-8').decode('utf-8')
            section = section.replace('@@PICT@@', table_str, 1)
            # delete 11 subsequent @@PICT@@
            section = section.replace('<text>@@PICT@@</text>', '', 11)


        if '@@PICT@@' in section:
            i = 0
            def replacement(match):
                nonlocal i
                i += 1
                return '<img src="./{}-{}.jpeg" />'.format(num, i)

            section = pict_re.sub(replacement, section)

        out.append(section)

    if Tables.xpath('section/table[not(@inserted)]'):
        import ipdb
        ipdb.set_trace()
        raise Exception('some tables not inserted')

    out = '<section>\n'.join(out).encode('utf-8')
    dom = etree.fromstring(out)

    with open(dst_file, 'wb') as f:
        f.write(etree.tostring(dom, pretty_print=True, encoding="utf-8"))

if __name__ == '__main__':
    insert_tables()
