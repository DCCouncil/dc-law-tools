from elasticsearch import Elasticsearch
import os
from universalclient import Client

DIR = os.path.abspath(os.path.dirname(__file__))

bld_file = os.path.join(DIR, '../working_files/dccode-html-bld.xml')
index_file = os.path.join(DIR, '../../dc-law-html/index.bulk')
schema_file = os.path.join(DIR, 'schema.json')

def click(group):
    @group.command()
    def index():
        update_index()

def update_index():
    es = Client('http://localhost:9200')
    es.dc.DELETE()
    with open(schema_file) as f:
        es.dc.POST(data=f.read())
    with open(index_file) as f:
        while True:
            lines = f.readlines(10000000)
            if not lines:
                break
            resp = es._bulk.POST(data=''.join(lines))
            # need to handle errors
