import re
import lxml.etree as et
from .utils import xstring, xcache, update_cache, make_node, process_up, process_down, process_xpath, pluralize

def add_no_page_flag(node):
    no_page_node = make_node('noPage', 'true')
    update_cache(node, no_page_node)

def add_titles(node):
    if node.tag == 'document':
        return
    prefix = xstring(node, '../@childPrefix')
    title = ''
    if prefix:
        title += prefix + ' '
    title += xstring(node, 'heading') or xstring(node, '@name')

    title_node = make_node('title', text=title)
    update_cache(node, title_node)

def add_url(node):
    if node.tag == 'library':
        url = '/'
    else:
        url = xcache(node.getparent(), 'url')
        prefix = xstring(node, '../@childPrefix')
        if prefix:
            url += pluralize(prefix).lower() + '/'
        url += xstring(node, '@name') + '/'

    url_node = make_node('url', url)
    update_cache(node, url_node)

def add_ancestors(node):
    if node.tag in ['collection']:
        ancestors = make_node('ancestors')
        for ancestor in node.xpath('../cache/ancestors/ancestor'):
            make_node('ancestor', parent=ancestors, **ancestor.attrib)
        if not xcache(node.getparent(), 'noPage'):
            parent_node = make_node('ancestor', parent=ancestors,
                                    url=xstring(node, '../cache/url'),
                                    title=xstring(node, '../cache/title'),
                                   )
        update_cache(node, ancestors)

library = (
    '/library',
    # process_xpath(
    #     (
    #         '/library/collection',
    #     ),
    #     add_no_page_flag,
    # ),
    process_down(
        add_titles,
        add_url,
        add_ancestors,
        valid_nodes=['library', 'collection'],
    ),
)

