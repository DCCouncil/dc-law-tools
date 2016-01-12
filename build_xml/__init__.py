from .insert_tables import insert_tables
from .process_annotations import process_annotations
from .split_up import split_up
from collections import OrderedDict

jobs = OrderedDict({
	'insert_tables': insert_tables,
	'process_annotations': process_annotations,
	'split_up': split_up,
})

def click(group):
	@group.group()
	def xml():
		pass

	for job_name, job in jobs.items():
		xml.command(name=job_name)(job)

	@xml.command()
	def all():
		for job in jobs.values():
			job()
