#!/usr/bin/env python
"""
process_annotations takes the output from process_annotations.py
and processes all the annotations into computer-readable,
structured data, rather than a bunch of human-readable text.

It runs all the transforms defined in annotation_transforms.

To add a new transform, add it to the list defined in
./annotation_transforms/__init__.py
"""


import os.path
import lxml.etree as et
from .annotation_transforms import transforms

DIR = os.path.abspath(os.path.dirname(__file__))

src_file = DIR + '/../working_files/dccode-no-placeholders.xml'
dst_file = DIR + '/../working_files/dccode-annotated.xml'


def process_annotations():
    parser = et.XMLParser(remove_blank_text=True)
    print('processing annotations...')
    with open(src_file) as f:
        dom = et.parse(f, parser)

    # XXX Start
    import re
    import click

    intra_cite_str = r'(?:ch\.? (?P<chapter>\w+),?\s*)?(?:ch\.? (?P<chapter2>\w+),?\s*)?(?:title (?P<title>\w+),?\s*)?' + \
                     r'(?:§{1,2} (?P<section>[^(\s]+)\s*(?P<subsections>(?:\([^\)]+\))*))?(?:par\. (?P<paragraph>\w+))?,?\s*' + \
                     r'(?P<more_cites>(?:(?:[^(\s]+)\s*(?:(?:\([^\)]+\))*))?[,$])*)'

    as_added_re = re.compile(r'[;,]?\s*(as\s*added\s*)+[;,]?\s*')
    def prep_hist_entry(h):
        h = h.strip('()')
        h = h.replace('\u2002', ' ').replace('\u2009', ' ').replace(' ', ' ') # replace a bunch of unicode almost-spaces with actual spaces
        h = ' '.join(h.split(' ')) # normalize to a single space
        h = as_added_re.sub('; as added ', h)
        h = h.split(';')
        h = [{'s': e, 'ws': e.strip()} for e in h]
        return h

    keywords = (
        ('added', 'as added by'),
        ('added', 'as added',),
        # ('repealed', 'repealed pursuant to'),
        ('repealed', 'repealed'),
        ('enacted', 'enacted'),
        ('renumbered_re', [re.compile(r'renumbered( as)? §\s*(?P<renumbered>\w*)', re.I)]),
        ('renumbered', 'renumbered'),
        ('restored_re', [re.compile(r'restored as §\s*(?P<restored>[\w()]*)')]),
        ('redesignated_re', [re.compile(r'redesignated §\s*(?P<redesignated>[\w()]*)')]),
        ('designated_re', [re.compile(r'designated as §\s*(?P<designated>[\w()]*)')]),
        ('amended', 'and amended'),
        ('citeless', [re.compile('(?P<partial_cite>' + re.sub(r'\?P\<[^>]+\>', '', intra_cite_str) + ')')]),
    )

    def parse_keywords(s):
        for key, match in keywords:
            if type(match) != str:
                out = parse_keyword(s, *match)
                if out:
                    return out
            elif s.startswith(match):
                return {key: True, 'ws': s[len(match):].strip(', ')}

        return {}

    def parse_keyword(string, *regexes):
        for regex in regexes:
            match = regex.match(string)
            if match:
                out = {'ws': regex.sub('', string, count=1).strip(', ')}
                out.update(match.groupdict())
                return out
        return {}

    date_re = re.compile(r'(?P<month>jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s*[.,]?\s*(?P<day>\d{1,2})\s*,?\s*(?P<year>[12]\d\d\d),?\s*', re.I)
    date_hash = {'jan': '1', 'feb': '2', 'mar': '3', 'apr': '4', 'may': '5', 'jun': '6', 'jul': '7', 'aug': '8', 'sep': '9', 'oct': '10', 'nov': '11', 'dec': '12'}
    def parse_date(s):
        match = date_re.match(s)
        if match:
            date_parts = match.groupdict()
            date_parts['month'] = date_hash[date_parts['month'].lower()]
            date = '{year}-{month}-{day}'.format(**date_parts)
            return {'date': date_parts, 'ws': date_re.sub('', s, count=1)}
        else:
            return {}

    def parse(string, key, *regexes):
        for regex in regexes:
            match = regex.search(string)
            if match:
                return {key: match.groupdict(), 'ws': regex.sub('', string, count=1)}
        return {}

    def run_parsers(string, regexes):
        out = {'ws': string}
        for key, regex in regexes.items():
            out.update(parse(out['ws'], key, *regex))
            out['ws'] = out['ws'].strip('., ')
        return out

    regexes = {
        'stat':         [re.compile(r'(?P<volume>\d+[\w]*)\s+Stat\.?\s+(?P<page>\d+(?:[-\s]\d+)?),?\s*' + intra_cite_str, re.I)],
        'law':          [   
                            re.compile(r'(?P<type>pub(?:lic)?|priv(?:ate)?)\.?\s*l(?:aw)?\.?(?:\s*No\.?)?' +
                                r' +(?P<congress>\d+)[-–\s]+(?P<number>\d+),?\s*' + 
                                intra_cite_str, re.I),
                            re.compile(r'(?:section (?P<section>\d+[\w\d\-]*)(?P<subsections>(?:\([^\)]+\))*) of )?' +
                                r'(?P<type>pub(?:lic)?|priv(?:ate)?)\.?\s*l(?:aw)?\.?(?:\s*No\.?)?' +
                                r' +(?P<congress>\d+)[-–\s]+(?P<number>\d+)', re.I)
                        ],
        'hr':           [re.compile(r'H\.?R\.?\s*(?P<number>\w+)\s*(?:§\s*(?P<section>\d+[\w\d\-]*)(?P<subsections>(?:\([^\)]+\))*))', re.I)],
        'ex_ord':       [re.compile(r'Ex\.?\s*Ord\.?\s*No\.\s*(?P<number>\w+),?\s*§\s*(?P<section>\w+)', re.I)],
        'dc_law':       [
                            re.compile(r'D\.?C\.?\s+Law\s+(?P<session>\d+)\s?[-–]+\s?(?P<number>\d+\w?),\s*' +
                                r'(?P<section>\d+[\w\d\-]*)\s*(?P<subsections>(?:\([^\)]+\))+)', re.I),
                            re.compile(r'D\.?C\.?\s+Law\s+(?P<session>\d+)\s?[-–]+\s?(?P<number>\d+\w?),?\s*' +
                                r'(?:§{1,2}\s*(?P<section>\d+[\w\d\-]*)\s*(?P<subsections>(?:\([^\)]+\))*)),?\s*' +
                                r'(?P<more_sections>(?:\d+[\w\d\-]*)\s*(?:(?:\([^\)]+\))*),\s*)*', re.I),
                            re.compile(r'D\.?C\.?\s+Law\s+(?P<session>\d+)\s?[-–]+\s?(?P<number>\d+\w?),?\s*' +
                                r'title (?P<title>\w+),?\s*(?:§\s*(?P<section>\d+[\w\d\-]*)\s*(?P<subsections>(?:\([^\)]+\))*)),?\s*(?:formerly\s*§\s*(?P<former_section>\w*))?', re.I)
                        ],
        'dc_reorg':     [
                            re.compile(r'(?P<year>\d{4}) reorg\. plan no\. (?P<number>\w+),?\s*' + intra_cite_str, re.I),
                            re.compile(r'reorg\. plan no\. (?P<number>\w+)(?: of)? \(?(?P<year>\d{4})\)?,?\s*' + intra_cite_str, re.I)
                        ],
        'dc_rev_stat':  [re.compile(r'R\.S\., D\.C\.,?\s*§\s*(?P<section>\d+)', re.I)],
        'dc_register':  [re.compile(r'(?P<volume>\d+)\s+DCR\s+(?P<page>\d+\w*)', re.I)],
    }

    hist = dom.xpath('//annoGroup[heading/text()="History"]/text[1]/text()')
    hist = [prep_hist_entry(h) for h in hist]
    cites = [c for h in hist for c in h]
    # cites = []
    # # split up "as added" into two cites
    # for cite in raw_cites:
    #     added_cite = None
    #     if 'as added' in cite:
    #         split_cite = [x.strip() for x in cite.split('as added')]
    #         if split_cite[0]:
    #             cites.append({'s': split_cite, 'ws': split_cite})
    #         elif not split_cite[1]
    #         try:
    #             added_cite = split_cite[1] or split_cite[2]
    #         except IndexError:

    #             import ipdb
    #             ipdb.set_trace()
    #         cites.append({'s': added_cite, 'ws': added_cite.strip(), 'added': True})
    #     else:
    #         cites.append({'s': cite, 'ws': cite.strip()})
            
    
    for cite in cites:
        cite.update(parse_keywords(cite['ws'].strip()))
        cite.update(parse_keywords(cite['ws'].strip()))
        cite.update(parse_date(cite['ws'].strip()))
        cite.update(run_parsers(cite['ws'], regexes))
        if not cite['ws'].strip('()., '):
            cite['ws'] = ''

    ws = [[x['ws'], x['s']] for x in cites if x['ws']]
    ln = len(ws)
    def sm(start=0, count=10):
        return ws[start:min(start+count, len(ws))]

    def smd(start=0, count=10):
        sample = sm(start, count)
        pad_to = min(max([len(x[0]) for x in sample]) + 2, 35)
        for item in sample:
            first = click.style(item[0], fg='red') + (' ' * (pad_to - len(item[0])))
            errors = [i for i in item[0].split(' ') if i]
            second = item[1]
            for error in errors:
                second = second.replace(error, click.style(error, 'red'))
            click.echo(first + second)
    click.echo(click.style('------', fg='green'))
    click.echo(click.style(str(ln), fg='green'))
    click.echo(click.style('------', fg='green'))
    import ipdb
    ipdb.set_trace()
    # XXX End


    for transform in transforms:
        transform(dom)

    with open(dst_file, 'wb') as f:
        f.write(et.tostring(dom, pretty_print=True, encoding="utf-8"))

if __name__ == '__main__':
    process_annotations()
