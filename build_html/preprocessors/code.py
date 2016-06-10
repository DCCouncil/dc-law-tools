import re, os
import lxml.etree as et
from copy import deepcopy
from .utils import xstring, xcache, update_cache, make_node, process_up, process_down, process_xpath, pluralize, resolve_ref, add_ancestors, index_doc_id, format_date

DIR = os.path.abspath(os.path.dirname(__file__))
xslt_partials_file = os.path.join(DIR, 'templates/section.xslt')

base_code_url = '/dc/council/code/'

with open(xslt_partials_file, 'r') as f:
    template = et.XSLT(et.parse(f))

def add_recency(node):
    recency = deepcopy(node.find('meta/recency'))
    for typ in ['law', 'emergency', 'federal']:
        effective = recency.find('{}/effective'.format(typ))
        effective.text = format_date(effective.text)
    update_cache(node, recency)
    xhtml = template(node.find('cache/recency')).getroot()
    update_cache(node, xhtml)

def prep_history(node):
    ref_node = resolve_ref(node)
    if ref_node is None:
        return
    node.set('url', xcache(ref_node, 'url'))

def add_no_page_flag(node):
    no_page_node = make_node('noPage', 'true')
    update_cache(node, no_page_node)

def add_titles(node):
    title_node = make_node('title', make_title(node))
    update_cache(node, title_node)

def make_title(node):
    level_type = node.tag
    title = ''

    if level_type == 'section':
        # this is a section, so show '§ XX-YY'.
        num = xstring(node, 'num')
        title = '§ {}. '.format(fix_section_dashes(num))
    elif level_type == 'container':
        # 'Division I', 'Title 10', 'Part XXX', etc.
        prefix = xstring(node, '../@childPrefix')
        num = xstring(node, 'num')
        title = '{} {}. '.format(prefix, num)

    # Concatenate the level's heading text.
    title += xstring(node, 'heading')
    title = title.strip()

    # if there's a reason, display it
    reason = xstring(node, 'reason')
    if reason:
        title += ' [' + reason + ']'
        
    return title

section_dashes_re = re.compile(r'^(\d+)-')
def fix_section_dashes(str):
    # Convert hyphens found in section numbers to en-dashes.
    # Only replace the first hyphen, which separates the title number.
    # Other hyphens are hyphens within section numbers and are hyphens?
    return section_dashes_re.sub(r'\1–', str)

sec_num_split_re = re.compile(r'[-:]')
def add_url(node):
    if node.tag == 'document':
        url = base_code_url
    elif node.tag == 'section':
        url = base_code_url + 'sections/{}.html'.format(xstring(node, 'num'))
    elif node.tag == 'container' and not xcache(node, 'noPage'):
        url = xcache(node.getparent(), 'url')
        prefix = xstring(node, '../@childPrefix')
        if prefix:
            url += pluralize(prefix).lower() + '/'
        url += xstring(node, 'num') + '/'
    else:
        url = xcache(node.getparent(), 'url')
    url_node = make_node('url', url)
    update_cache(node, url_node)

make_sibling_attribs = lambda node: {'url': xcache(node, 'url'), 'title': xcache(node, 'title')}
def add_siblings(node):
    if node.tag == 'document':
        siblings = make_node('siblings')
    elif xcache(node, 'noPage'):
        # next is correct for children, but prev is not
        siblings = deepcopy(node.find('../cache/siblings'))
    else:
        siblings = make_node('siblings')
        parent_node = node.getparent()
        prev_node = node.getprevious()
        # if previous sibling exists, then go to sibling
        if prev_node.tag in ['container', 'section']:
            make_node('prev', parent=siblings, **make_sibling_attribs(prev_node))
        # if parent has no page, then go to grandparent
        elif xcache(parent_node, 'noPage'):
            make_node('prev', parent=siblings, **make_sibling_attribs(parent_node.getparent()))
        # otherwise, just go to parent
        else:
            make_node('prev', parent=siblings, **make_sibling_attribs(parent_node))
        next_node = node.getnext()
        # if next sibling exists, then go to sibling
        if next_node.tag in ['container', 'section']:
            make_node('next', parent=siblings, **make_sibling_attribs(next_node))
        # otherwise, go to parent's next, if it exists
        else:
            next_cache = node.find('../cache/siblings/next')
            if next_cache is not None:
                siblings.append(deepcopy(next_cache))
    update_cache(node, siblings)

def add_bookend_sections(node):
    if node.tag == 'container':
        sec_start = node.xpath('string(section[1]/num | container[1]/cache/section-start)')
        sec_start_node = make_node('section-start', sec_start)
        update_cache(node, sec_start_node)
        sec_end = node.xpath('string(section[last()]/num | container[last()]/cache/section-end)')
        sec_end_node = make_node('section-end', sec_end)
        update_cache(node, sec_end_node)

def add_abs_id(node):
    node.set('id', xstring(node, 'num'))
    index_doc_id(node)

def make_section_html(node):
    xhtml = template(node).getroot()
    if xhtml is not None:
        update_cache(node, xhtml)

def replace_cite(node):
    ref_node = resolve_ref(node)
    if ref_node is None:
        return

    node.tag = 'a'
    for k in node.attrib.keys():
        del node.attrib[k]
    node.set('class', 'internal-link')
    node.set('href', xcache(ref_node, 'url'))

code = (
    '//document[@id="D.C. Code"][1]',
    process_xpath(
        './/container[../@childPrefix = "Division" or ../@childPrefix = "Subtitle"]',
        add_no_page_flag,
    ),
    process_xpath(
        '.',
        add_recency,
    ),
    process_xpath(
        './/annotation[@doc]',
        prep_history,
    ),
    process_down(
        add_titles,
        add_url,
        add_ancestors,
        valid_nodes=['document', 'container', 'section'],
    ),
    process_down(
        add_siblings,
        valid_nodes=['document', 'container', 'section'],
    ),
    process_up(
        add_bookend_sections,
        valid_nodes=['document', 'container'],
    ),
    process_xpath(
        './/section',
        add_abs_id,
        make_section_html,
    ),
    process_xpath(
        './/div//cite',
        replace_cite,
    ),
)

