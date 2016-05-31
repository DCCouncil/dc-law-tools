from .merge_xml import merge_xml
from .preprocess_xml import preprocess_xml
from .template_xml import template_xml
from collections import OrderedDict

jobs = OrderedDict((
	('merge_xml', merge_xml,),
	('preprocess_xml', preprocess_xml,),
	('template_xml', template_xml,),
))

def click(group):
	@group.group()
	def html():
		pass

	for job_name, job in jobs.items():
		html.command(name=job_name)(job)

	@html.command()
	def all():
		for job in jobs.values():
			job()
