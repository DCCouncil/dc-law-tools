"""
There are ~3000 unique headings in the raw code.
There are only about 40 semantically distinct headings.

This script normalizes all the headings to one of those
~40 headings.
"""

from pprint import pprint

def normalize_headings (dom):
    print('  normalizing headings...')
    heading_nodes = dom.xpath('//annoGroup/heading')

    for heading_node in heading_nodes:
        raw_txt = heading_node.text
        txt = raw_txt.lower()
        txt = normalized_headings.get(txt, txt) # default to the plain text, if not in normalized_headings

        if isinstance(txt, dict):
            update_node(heading_node, txt['heading'], txt['prepend'])
        elif txt in to_combine:
            combine_anno_node_with_previous_sibling(heading_node)
        elif txt in to_delete:
            delete_anno_node(heading_node)
            # TODO: delete node
        elif txt.startswith('legislative history of'):
            update_node(heading_node, 'Legislative History', raw_txt)
        elif txt.startswith('expiration of'):
            update_node(heading_node, 'Expiration of Law', raw_txt)
        elif txt.startswith('repeal of'):
            update_node(heading_node, 'Repeal of Law', raw_txt)
        elif txt.startswith('construction of'):
            update_node(heading_node, 'Construction of Law', raw_txt)
        else:
            update_node(heading_node, txt)

    final_heading_nodes = {}
    for node in dom.xpath('//annoGroup/heading'):
        final_heading_nodes.setdefault(node.text, 0)
        final_heading_nodes[node.text] += 1
    correct_headings = {"Mayor's Orders", 'Delegation of Authority', "Editor's Notes", 'Temporary Addition of Subchapter', 'History', 'New Implementing Regulations', 'Temporary Amendment of Section', 'Uniform Commercial Code Comment', 'Change in Government', 'Section References', 'Cross References', 'Temporary Addition of Section', 'Expiration of Law', 'Temporary Repeal of Section', 'Effect of Amendments', 'References in Text', 'Construction of Law', 'Short Title', 'Temporary Legislation', 'Severability of Law', 'Transfer of Functions', 'Congressional Disapproval of Acts of the Council', 'Prior Codifications', 'Emergency Legislation', 'Resolutions', 'Omission of Text', 'Repeal of Law', 'Legislative History', 'Effective Dates'}
    diff = set(final_heading_nodes) - correct_headings
    if diff:
        raise Exception('headings have changed: {}'.format(diff))
    return dom

def update_node(heading_node, heading_txt, prepend_txt=None):
    anno_node = heading_node.getparent()
    heading_node.text = heading_txt

    if prepend_txt is not None:
        prepend_txt_node = anno_node.makeelement('text')
        prepend_txt_node.text = prepend_txt
        heading_node.addnext(prepend_txt_node)

def combine_anno_node_with_previous_sibling(heading_node):
    anno_node = heading_node.getparent()
    prev_anno_node = anno_node.getprevious()
    for child_node in anno_node.getchildren():
        new_child = prev_anno_node.makeelement('text')
        new_child.text = child_node.text
        prev_anno_node.append(new_child)
    delete_anno_node(heading_node)

def delete_anno_node(heading_node):
    anno_node = heading_node.getparent()
    anno_node.getparent().remove(anno_node)

to_combine = [
  "report delineating actions taken to implement multiyear budget spending reduction and support act: -",
  "*****",
  
]

to_delete = [
  "temporary amendments of heading",
]

normalized_headings = {
  "amendment notes": "Effect of Amendments",
  "application of law": "Editor's Notes",
  "change in government": "Change in Government",
  "congressional disapproval of acts of the council": "Congressional Disapproval of Acts of the Council",
  "construction of emergency legislation": "Emergency Legislation",
  "cross references": "Cross References",
  "delegation of authority": "Delegation of Authority",
  "editor's note": "Editor's Notes",
  "editor's notes": "Editor's Notes",
  "editor's notes -": "Editor's Notes",
  "editor’ notes": "Editor's Notes",
  "editor’s note": "Editor's Notes",
  "editor’s notes": "Editor's Notes",
  "editor’s notes -": "Editor's Notes",
  "effect of amendments": "Effect of Amendments",
  "effect of amendments -": "Effect of Amendments",
  "effective dates": "Effective Dates",
  "effects of amendments": "Effect of Amendments",
  "emergency legislation": "Emergency Legislation",
  "emergency notes": "Emergency Legislation",
  "exchange of title over reservation 13": {"heading": "Editor's Notes", "prepend": "Exchange of Title over Reservation 13"},
  "historical citations": "Prior Codifications",
  "prior codifications": "Prior Codifications",
  "prior codification": "Prior Codifications",
  "history": "History",
  "law reviews and journal commentaries": "Law Reviews and Journal Commentaries",
  "legislaative history of law 20-154": "legislative history of law 20-154",
  "legislataive history of law 20-154": "legislative history of law 20-154",
  "mayor's orders": "Mayor's Orders",
  "mayor’s orders": "Mayor's Orders",
  "new implementing regulations": "New Implementing Regulations",
  "note regarding enactment of title 29": {"heading": "Editor's Notes", "prepend": "Note Regarding Enactment of Title 29"},
  "omission of text": "Omission of Text",
  "purpose of law 11-241": {"heading": "Editor's Notes", "prepend": "Purpose of Law 11-241"},
  "references in text": "References in Text",
  "resolutions": "Resolutions",
  "section references": "Section References",
  "severability of law": "Severability of Law",
  "short title": "Short Title",
  "temporary addition of section": "Temporary Addition of Section",
  "temporary addition of subchapter": "Temporary Addition of Subchapter",
  "temporary amendment of section": "Temporary Amendment of Section",
  "temporary amendments of section": "Temporary Amendment of Section",
  "temporary legislation": "Temporary Legislation",
  "temporary legislation -": "Temporary Legislation",
  "temporary repeal of section": "Temporary Repeal of Section",
  "termination of law": "Expiration of Law",
  "termination of law 6-10": "expiration of law 6-10",
  "transfer of functions": "Transfer of Functions",
  "uniform commercial code comment": "Uniform Commercial Code Comment"
}

