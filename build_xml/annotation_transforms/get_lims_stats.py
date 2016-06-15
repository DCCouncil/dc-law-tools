from universalclient import Client, jsonFilter
import json, click, re, os


DIR = os.path.abspath(os.path.dirname(__file__))
lims_data_path = os.path.join(DIR, 'lims_data.json')

lims = Client('http://lims.dccouncil.us/api/v1/', headers={'Content-Type': 'application/json'}, dataFilter=jsonFilter)

leg_details = lims.Legislation.Details._('{}')

leg_search = lims.Legislation.AdvancedSearch._('100/{}').data({"LegislationStatus": "130"})

out = json.load(open(lims_data_path))
# offset = int(len(out)/100)
# while True:
# 	leg_data = leg_search.POST(offset).json()
# 	print('getting:', offset*100, '-', offset*100+len(leg_data))
# 	with click.progressbar(leg_data) as leg_data_bar:
# 		for leg_datum in leg_data_bar:
# 			leg_number = leg_datum['LegislationNumber']
# 			leg = leg_details.GET(leg_number).json()
# 			out[leg_number] = leg
# 	offset += 1
# 	json.dump(out, open(lims_data_path, 'w'), sort_keys=True, indent=2)
# 	if not leg_data:
# 		print('completed')
# 		break

rawLawRegex = re.compile(r'(?:P\.)?([A-Z]*)(?:\. ?)?0*(\d+)-0*(\d+)')
for k, law in out.items():
	if law['Legislation'] is None:
		print('skipping', k)
		continue

	rawLawNum = law['Legislation']['LawNumber']
	try:
		parsedLawNum = rawLawRegex.match(rawLawNum).groups()
	except:
		print('skipping', rawLawNum)
	if parsedLawNum[0] != 'L':
		print('skipping: ', rawLawNum)
		continue
	lawNum = '{}-{}'.format(*parsedLawNum[1:])
	new_law = {
		'lawNum': lawNum,
		'dcLaw': {
			'period': parsedLawNum[1],
			'lawId': parsedLawNum[2],
		},
	}
	if law['CongressReview'][-1]['LawEffectiveDate']:
		law['date'] = law['CongressReview'][-1]['LawEffectiveDate'],
	if law['Legislation']['ShortTitle']:
		new_law['shortTitle'] = law['Legislation']['ShortTitle']
	docUrl = law['MayorReview'][-1].get('DocumentUrl')
	if docUrl:
		new_law['dcLaw']['url'] = docUrl
	if law['MayorReview'][-1]['Volume'] and law['MayorReview'][-1]['Page']:
		new_law['dcRegister'] = {
			'vol': str(law['MayorReview'][-1]['Volume']),
			'page': str(law['MayorReview'][-1]['Page']),
		}
	new_law['limsUrl'] = 'http://lims.dccouncil.us/Legislation/' + k
	law['normalized'] = new_law

json.dump(out, open(lims_data_path, 'w'), sort_keys=True, indent=2)