import os
from collections import OrderedDict
from .insert_t1_ch15 import insert_t1_ch15, src_file as src_insert_t1_ch15, dst_file as dst_insert_t1_ch15
from .insert_tables import insert_tables, src_file as src_insert_tables, dst_file as dst_insert_tables
from .split_placeholders import split_placeholders, src_file as src_split_placeholders, dst_file as dst_split_placeholders
from .process_annotations import process_annotations, src_file as src_process_annotations, dst_file as dst_process_annotations
from .add_cites import add_cites, src_file as src_add_cites, dst_file as dst_add_cites
from .split_up import split_up, src_file as src_split_up, dst_dir as dst_split_up

jobs = OrderedDict((
	('insert_t1_ch15', insert_t1_ch15,),
	('insert_tables', insert_tables,),
	('split_placeholders', split_placeholders,),
	('process_annotations', process_annotations,),
	('add_cites', add_cites,),
	('split_up', split_up,),
))

dst_file = ''
for job_name , job in jobs.items():
	if dst_file:
		src_file = os.path.normpath(globals().get('src_' + job_name))
		if dst_file != src_file:
			raise(BaseException('job {} has mismatched source. src: {}; dst: {}'.format(job_name, src_file, dst_file)))
	dst_file = os.path.normpath(globals().get('dst_' + job_name))


def click(group):
	@group.group()
	def xml():
		pass

	i = 1
	for job_name, job in jobs.items():
		xml.command(name='{}_{}'.format(i, job_name))(job)
		i += 1

	@xml.command()
	def all():
		for job in jobs.values():
			job()
