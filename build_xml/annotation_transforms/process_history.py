"""
History entries are a mess.
They do not conform to the style guidelines.
applies manual hist_string_fixes.json to pathological hist strings.
then parses each history entry using a PEG parser.
It then uses the generated AST to pull out useful info.

Right now it:
  - generates dc statutes. 
"""
import re, os, json
import click
from arpeggio import NoMatch
from .hist_analyzer import analyze_history
from collections import OrderedDict
import lxml.etree as et
DIR = os.path.abspath(os.path.dirname(__file__))

MANUAL_FIX = False

def process_history(dom):
    print('  processing history...')

    from .hist_parser import parser

    with open(os.path.join(DIR, 'hist_string_fixes.json'), 'r') as f:
        hist_string_fixes = json.load(f)

    hist_fixes = hist_string_fixes['hist_fixes']
    cite_fixes = hist_string_fixes['cite_fixes']

    as_added_re = re.compile(r'[;,]?\s*(as\s*added\s*)+[;,]?\s*')
    as_amended_re = re.compile(r'[;,.]?\s*as\s*amended\s*[;,.]?\s*')
    def prep_hist_entry(full_hist):
        if full_hist in hist_fixes:
            h = hist_fixes[full_hist]
        else:
            h = full_hist
        h = h.strip('()')
        h = h.replace('\u2002', ' ').replace('\u2009', ' ').replace(' ', ' ') # replace a bunch of unicode almost-spaces with actual spaces
        h = ' '.join(h.split(' ')) # normalize to a single space
        h = as_added_re.sub('; as added ', h)
        h = as_amended_re.sub('; ', h)
        h = h.replace(', redesignated', '; redesignated')
        h = h.replace(', renumbered', '; renumbered')
        h = h.split(';')
        h = [e.strip().strip('.') for e in h if '1973 Ed' not in e]
        h = [{'s': e + ',', 'h': full_hist} for e in h]
        for entry in h:
            if entry['s'] in cite_fixes:
                entry['s'] = cite_fixes[entry['s']]
        return h
    hist = dom.xpath('//annoGroup[heading/text()="History"]/annotation[1]/text()')
    hist = [prep_hist_entry(h) for h in hist]

    cites = [c for h in hist for c in h]

    with click.progressbar(cites) as progress_cites:
        for i, cite in enumerate(progress_cites):
            cite['i'] = i
            if not cite['s']:
                continue
            try:
                cite['ast'] = parser.parse(cite['s'])
            except NoMatch as err:
                cite['err'] = str(err)
            else:
                cite['analysis'] = analyze_history(cite['ast'])

    dc_law_cites = [x for x in cites if 'dcLaw' in x.get('analysis', {}) or ('dcRegister' in x.get('analysis', {}) and not 'dcRule' in x.get('analysis', {}))]
    dc_laws = {}

    for cite in dc_law_cites:
        lawNum = cite['analysis'].get('lawNum', '')
        if type(lawNum) == list:
            import ipdb
            ipdb.set_trace()
            continue
        dc_laws.setdefault(lawNum, {'cites': []})['cites'].append(cite)

    # drop into debug if any dc law cites are missing dc law numbers
    # if len(dc_laws['']):
    #     import ipdb
    #     ipdb.set_trace()

    dc_law_data = [x for x in dc_laws.values()]

    for dc_law_datum in dc_law_data:
        try:
            analysis = merge_and_dedup(*[x['analysis'] for x in dc_law_datum['cites']])
        except:
            import ipdb
            ipdb.set_trace()
            continue
        if contains_set(analysis) or 'date' not in analysis:
            dc_law_datum['flag'] = True
        dc_law_datum['deduped_analysis'] = analysis

    dc_law_data.sort(key=get_normalized_dc_law_num)

    dc_law_errors = [x for x in dc_law_data if 'err' in x]

    if MANUAL_FIX:
        err = [x for x in cites if 'err' in x]
        good = [x for x in cites if 'err' not in x]
        len(cite)
        click.echo('------')
        click.echo('{} {} {}'.format(len(cite), click.style(str(len(good)), fg='green'), click.style(str(len(err)), fg='red')))
        click.echo('------')

        def sm(start=0, count=10):
            """ Sample errors. defaults to first 10 errors. """
            ignored_errors = {x[0]: x for x in hist_string_fixes['manual']}
            unignored_errors = [x for x in err if x['s'] not in ignored_errors]
            return unignored_errors[start:min(start+count, len(unignored_errors))]

        def smd(start=0, count=10):
            """ Display a sample of errors. Defaults to first 10 errors. """
            sample = sm(start, count)
            for item in sample:
                click.echo
                click.echo(click.style('    {}) {}'.format(item['i'], item['err']), fg='red'))
                click.echo(item['s'])

        err_dict = {x['i']: x for x in err}

        fix_changes = []

        def is_partial_cite(ast, depth=4):
            import ipdb
            ipdb.set_trace()
            if ast.rule_name == 'partialCite':
                return True
            if depth and hasattr(ast, '__getitem__'):
                for child in ast:
                    child_is_partial = is_partial_cite(child, depth=depth-1)
                    if child_is_partial:
                        return True
            return False

        def get_partial_cites(cites):
            return [cite for cite in cites if 'ast' in cite and is_partial_cite(cite['ast'])]


        def fix(index, new_string=None):
            """
            helper function. fix the single cite error at index.
            no new_string: display the "fix(index, old_string)" for manual modification.
            MUST CALL `save()` to save fixes.
            """

            cite_string = cites[index]['s']
            if new_string is None:
                return "fix({}, '{}')".format(index, cite_string)
            fix_changes.append(cite_string)
            cite_fixes[cite_string] = new_string

        def fix_hist(index, new_hist=None):
            """
            helper function. fix the entire hist string error at index.
            no new_hist: display the "fix(index, old_hist)" for manual modification.
            MUST CALL `save()` to save fixes.
            """
            hist = cites[index]['h']
            if new_hist is None:
                return "fix_hist({}, '{}')".format(index, hist)
            hist_fixes[hist] = new_hist

        def manual(*indices):
            """
            helper function. add a cite string for manual review.
            MUST CALL `save()`
            """
            for index in indices:
                cite_string = cites[index]
                hist_string_fixes['manual'].append([cite_string['s'], cite_string['s'], cite_string['h']])

        def manual_hist(*indices):
            """
            helper function. add an entire history string for manual review.
            MUST CALL `save().
            """
            for index in indices:
                cite_string = cites[index]
                hist_string_fixes['manual_hist'].append([cite_string['h'], cite_string['h'], cite_string['s']])

        def save():
            """
            helper function. save hist_string_fixes.json changes made by any
            of the above helper functions.
            """
            for item in hist_string_fixes['manual']:
                if item[0] != item[1]:
                    cite_fixes[item[0]] = item[1]
            hist_string_fixes['manual'] = [x for x in hist_string_fixes['manual'] if x[0] == x[1]]
            for item in hist_string_fixes['manual_hist']:
                if item[0] != item[1]:
                    hist_fixes[item[0]] = item[1]
            hist_string_fixes['manual_hist'] = [x for x in hist_string_fixes['manual_hist'] if x[0] == x[1]]
            with open(os.path.join(DIR, 'hist_string_fixes.json'), 'w') as f:
                json.dump(hist_string_fixes, f, indent=2)
        import ipdb
        ipdb.set_trace()
    merge_lims_data(dc_law_data)
    make_statutes(dom, dc_law_data)
    fix_history(dom, hist)

def merge_and_dedup(*dicts):
    """
    returns a deeply merged dict - any items that are not identical are turned into sets.
    """
    out = {}
    for d in dicts:
        for k, v in d.items():
            if k in out:
                if type(out[k]) == dict:
                    out[k] = merge_and_dedup(out[k], v)
                else:
                    if type(out[k]) != set:
                        out[k] = set([out[k]])
                    out[k].add(v)
                    if len(out[k]) == 1:
                        out[k] = list(out[k])[0]
            else:
                out[k] = v
    return out

def contains_set(d):
    """ return whether the dict contains a set; convert all sets to lists """
    out = False
    for k, v in d.items():
        if type(v) == set:
            d[k] = sorted(list(v))
            out = True
        elif type(v) == dict and contains_set(v):
            out = True
    return out

dc_law_num_re = re.compile(r'(\d+)-(\d+)(\w*)')
def get_normalized_dc_law_num(dc_law_datum):
    law_num = dc_law_datum['deduped_analysis'].get('lawNum', '0-0')
    parts = dc_law_num_re.match(law_num).groups()
    return '{0:0>3}-{1:0>4}{2}'.format(*parts)

def merge_lims_data(dc_law_data):
    lims_data = json.load(open(os.path.join(DIR, 'lims_data.json')))
    lims_data = prep_lims_data(lims_data)
    out = {}
    for dc_law in dc_law_data:
        deduped_analysis = dc_law['deduped_analysis']
        try:
            lawNum = deduped_analysis['lawNum']
        except:
            import ipdb
            ipdb.set_trace()
        if lawNum in lims_data:
            if 'flag' in dc_law:
                dc_law['deduped_analysis'] = lims_data[lawNum]
                continue
            deduped_analysis = merge_and_dedup(deduped_analysis, lims_data[lawNum])
            if contains_set(deduped_analysis):
                dc_law['flag'] = 'true'
            dc_law['deduped_analysis'] = deduped_analysis
            del lims_data[lawNum]

def prep_lims_data(lims_data):
    out = {}
    dedup = lims_data.pop('dedup')
    for billNum, v in lims_data.items():
        if 'normalized' in v:
            lawNum = v['normalized']['lawNum']
            if lawNum in dedup and dedup[lawNum] != billNum:
                continue
            out[lawNum] = v['normalized']
    return out

def fix_history(dom, hist):
    fixed_hist_nodes = [make_history_node(h) for h in hist]
    hist_nodes = dom.xpath('//annoGroup[heading/text()="History"]')

    for hist_node, fixed_hist_node in zip(hist_nodes, fixed_hist_nodes):
        hist_node.getparent().replace(hist_node, fixed_hist_node)

def make_history_node(fixed_hist_entries):
    fixed_hist_node = _make_node('annoGroup')
    _make_node('heading', fixed_hist_node, text='History')
    for fixed_hist_entry in fixed_hist_entries:
        text = fixed_hist_entry['s'].strip(',')
        attrs = {}
        lawNum = fixed_hist_entry.get('analysis', {}).get('lawNum', '')
        if lawNum:
            attrs['doc'] = 'D.C. Law {}'.format(lawNum)
        _make_node('annotation', fixed_hist_node, text=text, **attrs)
    return fixed_hist_node

def make_statutes(dom, dc_law_data):
    for dc_law in dc_law_data:
        if 'err' in dc_law:
            continue
        dc_law = dc_law['deduped_analysis']
        make_statute(dom, dc_law)

statute_root_node = None
def get_statute(dom, law_num):
    global statute_root_node
    if statute_root_node is None:
        statute_root_node = dom.find('//collection[@name="dclaws"]')
    return statute_root_node.find('collection/document[@id="D.C. Law {}"]'.format(law_num))

def make_statute(dom, dc_law):
    """
    {'lawNum', 'flag', 'shortTitle', 'effective', 'limsUrl', 'dcLaw': {'period', 'lawId', 'url'}, dcRegister: {'vol', 'page'}}
    """
    global statute_root_node
    # cache the statute root node to speed 
    if statute_root_node is None:
        statute_root_node = dom.find('//collection[@name="dclaws"]')
    law_node_attribs = {
        'id': 'D.C. Law {}'.format(dc_law['lawNum'])
    }
    if 'flag' in dc_law:
        law_node_attribs['flag'] = 'true'
    try:
        period_node = statute_root_node.find('collection[@name="{}"]'.format(dc_law['dcLaw']['period']))
    except:
        import ipdb
        ipdb.set_trace()
    try:
        law_node = _make_node('document', period_node, **law_node_attribs)
    except:
        import ipdb
        ipdb.set_trace()
    _make_node('num', law_node, dc_law['lawNum'], type='law')
    if 'shortTitle' in dc_law:
        _make_node('heading', law_node, dc_law['shortTitle'].strip('. '))
    date_node = _make_node('effective', law_node, dc_law.get('date', ''))
    cite_node = _make_node('cites', law_node)
    _make_node('law', cite_node, **dc_law['dcLaw'])
    if 'dcRegister' in dc_law:
        _make_node('register', cite_node, **dc_law['dcRegister'])
    if 'limsUrl' in dc_law:
        _make_node('history', law_node, url=dc_law['limsUrl'])
    return law_node

def _make_node(tag, parent=None, text='', children=[], **attributes):
    attrs = OrderedDict(sorted([(k, (v[0] if type(v) == list else v)) for k, v in attributes.items()]))
    node = et.Element(tag, attrs)
    if parent is not None:
        parent.append(node)
    for child in children:
        node.append(child)
    if text:
        if type(text) == list:
            node.text = text[0]
        else:
            node.text = text
    return node
