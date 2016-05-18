from arpeggio import PTNodeVisitor, visit_parse_tree
from .hist_parser import parser

def merge(*dicts):
	out = {}
	for d in dicts:
		for k, v in d.items():
			if k in out:
				if type(out[k]) != list:
					out[k] = [out[k]]
				out[k].append(v)
			else:
				out[k] = v
	return out

def merge_children(children):
	dictChildren = [x for x in children if type(x) == dict]
	out = merge({}, *dictChildren)
	return out

date_hash = {'jan': '1', 'feb': '2', 'mar': '3', 'apr': '4', 'may': '5', 'jun': '6', 'jul': '7', 'aug': '8', 'sep': '9', 'oct': '10', 'nov': '11', 'dec': '12'}

class BaseVisitor(PTNodeVisitor):
	def visit_SS(self, node, children):			return None
	def visit_oDot(self, node, children):		return None
	def visit_oComma(self, node, children):		return None
	def visit_oCot(self, node, children):		return None
	def visit_cot(self, node, children):		return None
	def visit_oDot(self, node, children):		return None
	def visit_dcToken(self, node, children):	return None
	def visit_usToken(self, node, children):	return None
	def visit_dcLawToken(self, node, children):	return None
	def visit_dash(self, node, children):		return None

	def visit_date(self, n, c):
		month = date_hash[c[0].lower()[:3]]
		return {'date': '{}-{}-{}'.format(c[2], month, c[1])}

	def visit_dcLaw(self, node, children):			return {'dcLaw': {'session': children[0], 'lawId': children[1]}, 'lawNum': '{}-{}'.format(*children[:2])}
	def visit_dcRegister(self, node, children):		return {'dcRegister': {'vol': children[0], 'page': children[2]}}
	def visit_ruleAmend(self, node, children):		return {'dcRule': True}

	def visit_keywords(self, node, children):		return merge_children(children)
	def visit_citeString(self, node, children):		return merge_children(children)

class getPartialCite(BaseVisitor):
	def visit_subSecs(self, node, children):	return {'subSecs': children}
	def visit_rawSec(self, node, children):		return merge({'sec': children[0]}, children[1])

	def visit_section(self, node, children):
		import ipdb
		ipdb.set_trace()
		first = children[0]
		for child in children[1:]:
			if 'sec' not in child:
				child['sec'] = first['sec']
			if child['sec'] == first['sec'] and len(first.get('subSecs', [])) > len(child.get('subSecs', [])):
				child['subSecs'] = first['subSecs'][:-len(child['subSecs'])] + child['subSecs']
		return children

	def visit_intraCite(self, node, children):
		return {'intra': children[0]}

	def visit_dcLaw(self, node, children):		
		import ipdb
		ipdb.set_trace()
		return {'cite': merge({'typ': 'dcLaw', 'num': children[0]}, children[1])}

	def visit_dcRegister(self, node, children):	return {'cite': {'typ': 'dcReg', 'vol': children[0], 'page': children[1]}}

	def visit_citeString(self, node, children):
		import ipdb
		ipdb.set_trace()

class HistVisitor(BaseVisitor):
	pass

def analyze_history(ast):
	return visit_parse_tree(ast, HistVisitor())

# <history>
# 	<entry id=124>
# 		<intra>
# 			<cite>§ 212</cite>
# 			<cite type='fed_stat'><page>1494</page></cite>
# 		</intra>
# 		<intra>
# 			<cite>§ 213</cite>
# 			<cite>22 fed stat 1498</cite>
# 		</intra>
# 	</entry>
# </history>


# <document id=123>
# 	<cite>D.C. Law 4-29</cite>
# 	<cite>28 DCR 3081</cite>
# </document>

# 22 fed stat 1494, 1498, pub law 31-25, §§ 212, 213

# <document id=124>
# 	<cite>pub law 31-25</cite>
# 	<cite type='fed_stat'>
# 		<vol>22</vol>
# 		<page>1484</page>
# 	</cite>
# </document>

