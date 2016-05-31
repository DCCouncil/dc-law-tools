import  lxml.etree as et
from .preprocessors import preprocessors
from .preprocessors.utils import index_docs
import os

DIR = os.path.abspath(os.path.dirname(__file__))

out_dir = os.path.join(DIR, '../../dc-law-html')
bld_file = os.path.join(DIR, '../working_files/dccode-html-bld.xml')

def preprocess_xml():
    print('preprocessing...')
    parser = et.XMLParser(remove_blank_text=True)
    with open(bld_file) as f:
        dom = et.parse(f, parser)
    index_docs(dom)

    for preprocessor in preprocessors:
        preprocess(dom, *preprocessor)
    with open(bld_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

def preprocess(dom, xpath, *preprocessors):
    roots = dom.xpath(xpath)
    if not roots:
        raise BaseException('no valid roots for xpath:', xpath)
    for root in roots:
        for preprocessor in preprocessors:
            preprocessor(root)

def pdfs(dom):
    pdf_dir = os.path.join(DIR, 'dc_laws')
    pdf_out_path = os.path.join(DIR, '../../dc-law-docs-laws/{}.pdf')
    pdfs = os.listdir(pdf_dir)
    law_root = dom.find('//collection[@name="dclaws"]')
    skip_laws = law_root.xpath('./collection/document[cites/law/@url]/num/text()')
    for pdf in pdfs:
        if not pdf.startswith('dc-law-docs-laws'):
            print('skipping', pdf)
            continue
        pdf_path = os.path.join(pdf_dir, pdf)
        law_num = pdf.replace('dc-law-docs-laws', '')[:-4]
        if law_num in skip_laws:
            continue
        os.rename(pdf_path, pdf_out_path.format(law_num))
    import ipdb
    ipdb.set_trace()