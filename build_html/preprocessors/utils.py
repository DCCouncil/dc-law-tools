import  lxml.etree as et
import moment

def process_xpath(xpaths, *preprocessors):
    def _process_xpath(root):
        nonlocal xpaths
        if type(xpaths) == str:
            xpaths = (xpaths,)
        for xpath in xpaths:
            nodes = root.xpath(xpath)
            if not nodes:
                import ipdb
                ipdb.set_trace()
                raise BaseException('no valid nodes for xpath:', xpath)
            for node in nodes:
                for preprocessor in preprocessors:
                    preprocessor(node)
    return _process_xpath

def process_down(*preprocessors, valid_nodes=None):
    def _process_down(root):
        for node in iter_down(root, valid_nodes):
            for preprocessor in preprocessors:
                preprocessor(node)
    return _process_down

def process_up(*preprocessors, valid_nodes=None):
    def _process_up(root):
        for node in iter_up(root, valid_nodes):
            for preprocessor in preprocessors:
                preprocessor(node)
    return _process_up

def iter_down(node, valid_nodes=None):
    yield node
    for child in node.iterchildren():
        if valid_nodes is None or child.tag in valid_nodes:
            for descendant in iter_down(child, valid_nodes):
                yield descendant

def iter_up(node, valid_nodes=None):
    for child in node.iterchildren():
        if valid_nodes is None or child.tag in valid_nodes:
            for descendant in iter_up(child, valid_nodes):
                yield descendant
    yield node

# ------------------------------------

plurals = {}
def pluralize(word):
    if word in plurals:
        return plurals[word]
    else:
        return word + 's'

id_index = {}

def index_docs(dom):
    global id_index
    for node in dom.xpath('//document[@id]'):
        id_index[xstring(node, '@id')] = {'node': node, 'children': {}}
    pass

def index_doc(doc_node, xpath='.//*'):
    global id_index
    doc_id = doc_node.get('id')
    doc_index = id_index.setdefault({'node': doc_node, 'children': {}})['children']
    xpath += '[@id]'
    for node in doc.xpath(xpath):
        doc_index[xstring(node, '@id')] = node

def index_doc_id(node):
    global id_index
    doc_node = node.xpath('ancestor::document')[0]
    doc_id = xstring(doc_node, '@id')
    node_id = xstring(node, '@id')
    id_index.setdefault(doc_id, {'node': doc_node, 'children': {}})['children'][node_id] = node

def resolve_ref(node):
    doc_id = node.get('doc') or xstring(node, 'ancestor::document/@id')

    doc_index = id_index.get(doc_id)
    if doc_index is None:
        print('invalid cite: ', doc_id or 'None')
        return

    abs_id = node.get('abs')
    if abs_id:
        ref_node = doc_index['children'].get(abs_id)
    else:
        ref_node = doc_index['node']

    if ref_node is None:
        print('invalid cite: ', doc_id or 'None', abs_id or 'None')
        
    return ref_node

# ------------------------------------

def format_date(date):
    return moment.date(date).strftime('%B %d, %Y')
# ------------------------------------
def xstring(node, xpath):
    return node.xpath('string({})'.format(xpath))

def xcache(node, tag):
    return xstring(node, 'cache/{}'.format(tag))

def update_cache(node, new_el, xpath=None):
    if node is None:
        return
    cache = node.find('cache')
    if cache is None:
        cache = make_node('cache', parent=node)
    if xpath is not None:
        cache = cache.find(xpath)
    if cache is None:
        raise Exception('path specified by xpath {} must exist'.format(xpath))
    try:
        old_el = cache.find(new_el.tag)
    except:
        import ipdb
        ipdb.set_trace()
    if old_el is None:
        cache.append(new_el)
    else:
        cache.replace(old_el, new_el)

def make_node(tag, text=None, parent=None, **attrs):
    """Make a node in an XML document."""
    n = et.Element(tag)
    if parent is not None:
        parent.append(n)
    n.text = text
    for k, v in attrs.items():
        if v is None: continue
        elif isinstance(v, (bool, int)):
            v = str(v)
        n.set(k.replace("___", ""), v)
    return n


def add_ancestors(node):
    ancestors = make_node('ancestors')
    for ancestor in node.xpath('../cache/ancestors/ancestor'):
        make_node('ancestor', parent=ancestors, **ancestor.attrib)
    if node.getparent() is not None and not xcache(node.getparent(), 'noPage'):
        parent_node = make_node('ancestor', parent=ancestors,
                                url=xstring(node, '../cache/url'),
                                title=xstring(node, '../cache/title'),
                               )
    update_cache(node, ancestors)
