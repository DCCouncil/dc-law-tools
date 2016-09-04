from utils import work_on_dom, work_on_files

import os, lxml.etree as et, re, glob

DIR = os.path.abspath(os.path.dirname(__file__))
repo_dir = os.path.join(DIR, '../../dc-law-xml')

def explore():
	with work_on_dom(repo_dir, interactive=True) as dom:
		pass

def rebuild():
	with work_on_dom(repo_dir) as dom:
		pass

def work_on_sections():
	for dom in work_on_files(repo_dir, 'dc/council/code/titles/*/sections/*.xml'):
		yield dom

def work_on_titles():
	for dom in work_on_files(repo_dir, 'dc/council/code/titles/*/index.xml'):
		yield dom

def work_on_law_indexes():
	for dom in work_on_files(repo_dir, 'dc/council/periods/*/laws/index.xml'):
		yield dom

def work_on_laws():
	for dom in work_on_files(repo_dir, 'dc/council/periods/*/laws/[0-9]*'):
		yield dom



law_key_re = re.compile(r'\./\d+-(\d+)(\w*)\.xml')
def resort_law_indexes():
	for dom in work_on_law_indexes():
		includes = dom.xpath('//collection/ns0:include', namespaces={'ns0': 'http://www.w3.org/2001/XInclude'})
		includes = sorted(includes, key=lambda i: '{:0>5}{}'.format(*law_key_re.search(i.get('href')).groups()))
		parent = includes[0].getparent()
		for include in includes:
			parent.remove(include)
			parent.insert(1, include)

period_re = re.compile('periods/(\d+)/laws/(.*)')
def rename_laws():
	for path in glob.glob(os.path.join(repo_dir, 'dc/council/periods/*/laws/[0-9]*')):
		period = period_re.search(path).groups()
		try:
			new_path = os.path.join(repo_dir, 'dc/council/periods/{0}/laws/{0}-{1}').format(*period)
		except:
			import ipdb
			ipdb.set_trace()
		os.rename(path, new_path)

section_key_re = re.compile(r'(\d*)(\w*)(\W*)(\d*)(\w*)(\W*)(\d*)(\w*)(\W*)(\d*)(\w*)(\W*)\.xml')
def get_section_key(i):
	out = ''
	match = section_key_re.search(i.get('href')).groups()
	for i, s in enumerate(match):
		if i % 3 != 2:
			out += '{:0>5}'.format(s)
	return out

def sort_section_includes():
	for dom in work_on_titles():
		leaf_containers = dom.xpath('//container[ns0:include]', namespaces={'ns0': 'http://www.w3.org/2001/XInclude'})
		for leaf_container in leaf_containers:
			includes = leaf_container.xpath('./ns0:include', namespaces={'ns0': 'http://www.w3.org/2001/XInclude'})
			includes = sorted(includes, key=get_section_key, reverse=True)
			already_included = set()
			for include in includes:
				leaf_container.remove(include)
			for include in includes:
				href = include.get('href')
				if href == './sections/1219.38.xml':
					import ipdb
					ipdb.set_trace()
				if href not in already_included:
					leaf_container.insert(2, include)
					already_included.add(href)

section_include_re = re.compile('/([^/]*).xml$')
def rename_include_hrefs():
	for dom in work_on_titles():
		includes = dom.xpath('//ns0:include', namespaces={'ns0': 'http://www.w3.org/2001/XInclude'})
		title = dom.find('num').text	
		separator = ':' if title == '28' else '-'
		for include in includes:
			path = include.get('href')
			new_path = section_include_re.sub(r'/{}{}\1.xml'.format(title, separator), path)
			include.set('href', new_path)

section_re = re.compile('/(\w+)/sections/(.*)')
def rename_sections():
	for path in glob.glob(os.path.join(repo_dir, 'dc/council/code/titles/*/sections/*')):
		title = section_re.search(path).groups()
		separator = ':' if title[0] == '28' else '-'
		new_path = os.path.join(repo_dir, 'dc/council/code/titles/{1}/sections/{1}{0}{2}').format(separator, *title)
		os.rename(path, new_path)
