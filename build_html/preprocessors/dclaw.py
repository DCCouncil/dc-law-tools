from .utils import xstring, xcache, update_cache, process_xpath, make_node, add_ancestors, format_date

def add_titles(node):
    title = short_title = xstring(node, '@id')
    heading = xstring(node, 'heading')
    if heading:
        title += '. {}.'.format(heading.strip('. '))
    title_node = make_node('title', title)
    update_cache(node, title_node)
    short_title_node = make_node('shortTitle', short_title)
    update_cache(node, short_title_node)

def add_url(node):
    url = '/dc/council/laws/{}.html'.format(xstring(node, 'num'))
    url_node = make_node('url', url)
    update_cache(node, url_node)

def add_dates(node):
    effective_date = xstring(node, 'effective')
    effective_date = format_date(effective_date) if effective_date else "Unknown"
    effective_node = make_node('effective', effective_date)
    update_cache(node, effective_node)

dclaw = (
    '//document[starts-with(@id, "D.C. Law")]',
    process_xpath(
        '.',
        add_titles,
        add_url,
        add_ancestors,
        add_dates,
    ),
)
