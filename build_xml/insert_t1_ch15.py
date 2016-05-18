import os.path
import lxml.etree as et

DIR = os.path.abspath(os.path.dirname(__file__))

src_file = DIR + '/../working_files/dccode.xml'
ch15_path = DIR + '/t1_ch15.xml'
dst_file = DIR + '/../working_files/dccode-t1-ch15.xml'

def insert_t1_ch15():
    parser = et.XMLParser(remove_blank_text=True)

    print('inserting title 1 chapter 15...')
    with open(src_file) as f:
        dom = et.parse(f, parser)
    with open(ch15_path) as f:
    	ch15 = et.parse(f, parser).getroot()

    title_1 = dom.xpath('/code/container[1]/container[1]')
    title_1.append(ch15)

    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))
