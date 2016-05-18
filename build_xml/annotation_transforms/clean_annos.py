

def clean_annos(dom):
	print('cleaning annotations')
	single_text_anno_groups = dom.xpath('//annoGroup[count(text)=1]')
	for anno_group in single_text_anno_groups:
		anno_group.find('text').tag = 'annotation'
	single_anno_headings = [
		'Cross References',
		'Prior Codifications',
		'Emergency Legislation',
		'Delegation of Authority',
		'Effect of Amendments',
		'Effective Dates',
		'Prior Codifications',
		'Temporary Amendment of Section',
		'Temporary Addition of Section',
		'Temporary Legislation',
		'Temporary Repeal of Section',
		'Temporary Addition of Subchapter',
	]

	for heading in single_anno_headings:
		anno_texts = dom.xpath('//annoGroup[heading="{}"]/text'.format(heading))
		for text_node in anno_texts:
			text_node.tag = 'annotation'
