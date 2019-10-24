# NOTE, some of the comments are in error as I've made fixes,
# or the filtering strategy is effectively handling it implicitly,
# there's a major need for DRY to be applied, it's not Pythonic,
# and so on. But I wanted to get this into source code control
# before a hard drive fries.



import urllib.parse as ul
import json

countries = {
'LAT': 'Latvia',
'ABW': 'Aruba',
'AFG': 'Afghanistan',
'AGO': 'Angola',
'AIA': 'Anguilla',
'ALA': 'Åland Islands',
'ALB': 'Albania',
'AND': 'Andorra',
'ARE': 'United Arab Emirates',
'ARG': 'Argentina',
'ARM': 'Armenia',
'ASM': 'American Samoa',
'ATA': 'Antarctica',
'ATF': 'French Southern and Antarctic Lands',
'ATG': 'Antigua and Barbuda',
'AUS': 'Australia',
'AUT': 'Austria',
'AZE': 'Azerbaijan',
'BDI': 'Burundi',
'BEL': 'Belgium',
'BEN': 'Benin',
'BES': 'Caribbean Netherlands',
'BFA': 'Burkina Faso',
'BGD': 'Bangladesh',
'BGR': 'Bulgaria',
'BHR': 'Bahrain',
'BHS': 'The Bahamas',
'BIH': 'Bosnia and Herzegovina',
'BLM': 'Saint Barthélemy',
'BLR': 'Belarus',
'BLZ': 'Belize',
'BMU': 'Bermuda',
'BOL': 'Bolivia',
'BRA': 'Brazil',
'BRB': 'Barbados',
'BRN': 'Brunei',
'BTN': 'Bhutan',
'BVT': 'Bouvet Island',
'BWA': 'Botswana',
'CAF': 'Central African Republic',
'CAN': 'Canada',
'CCK': 'Cocos (Keeling) Islands',
'CHE': 'Switzerland',
'CHL': 'Chile',
'CHN': 'China',
'CIV': 'Ivory Coast',
'CMR': 'Cameroon',
'COD': 'Democratic Republic of the Congo',
'COG': 'Republic of the Congo',
'COK': 'Cook Islands',
'COL': 'Colombia',
'COM': 'Comoros',
'CPV': 'Cape Verde',
'CRI': 'Costa Rica',
'CUB': 'Cuba',
'CUW': 'Curaçao',
'CXR': 'Christmas Island',
'CYM': 'Cayman Islands',
'CYP': 'Cyprus',
'CZE': 'Czech Republic',
'DEU': 'Germany',
'DJI': 'Djibouti',
'DMA': 'Dominica',
'DNK': 'Denmark',
'DOM': 'Dominican Republic',
'DZA': 'Algeria',
'ECU': 'Ecuador',
'EGY': 'Egypt',
'ERI': 'Eritrea',
'ESH': 'Western Sahara',
'ESP': 'Spain',
'EST': 'Estonia',
'ETH': 'Ethiopia',
'FIN': 'Finland',
'FJI': 'Fiji',
'FLK': 'Falkland Islands',
'FRA': 'France',
'FRO': 'Faroe Islands',
'FSM': 'Federated States of Micronesia',
'GAB': 'Gabon',
'GBR': 'United Kingdom',
'GEO': 'Georgia',
'GGY': 'Guernsey',
'GHA': 'Ghana',
'GIB': 'Gibraltar',
'GIN': 'Guinea',
'GLP': 'Guadeloupe',
'GMB': 'The Gambia',
'GNB': 'Guinea-Bissau',
'GNQ': 'Equatorial Guinea',
'GRC': 'Greece',
'GRD': 'Grenada',
'GRL': 'Greenland',
'GTM': 'Guatemala',
'GUF': 'French Guiana',
'GUM': 'Guam',
'GUY': 'Guyana',
'HKG': 'Hong Kong',
'HMD': 'Heard Island and McDonald Islands',
'HND': 'Honduras',
'HRV': 'Croatia',
'HTI': 'Haiti',
'HUN': 'Hungary',
'IDN': 'Indonesia',
'IMN': 'Isle of Man',
'IND': 'India',
'IOT': 'British Indian Ocean Territory',
'IRL': 'Ireland',
'IRN': 'Iran',
'IRQ': 'Iraq',
'ISL': 'Iceland',
'ISR': 'Israel',
'ITA': 'Italy',
'JAM': 'Jamaica',
'JEY': 'Jersey',
'JOR': 'Jordan',
'JPN': 'Japan',
'KAZ': 'Kazakhstan',
'KEN': 'Kenya',
'KGZ': 'Kyrgyzstan',
'KHM': 'Cambodia',
'KIR': 'Kiribati',
'KNA': 'Saint Kitts and Nevis',
'KOR': 'South Korea',
'KWT': 'Kuwait',
'LAO': 'Laos',
'LBN': 'Lebanon',
'LBR': 'Liberia',
'LBY': 'Libya',
'LCA': 'Saint Lucia',
'LIE': 'Liechtenstein',
'LKA': 'Sri Lanka',
'LSO': 'Lesotho',
'LTU': 'Lithuania',
'LUX': 'Luxembourg',
'LVA': 'Latvia',
'MAC': 'Macau',
'MAF': 'Collectivity of Saint Martin',
'MAR': 'Morocco',
'MCO': 'Monaco',
'MDA': 'Moldova',
'MDG': 'Madagascar',
'MDV': 'Maldives',
'MEX': 'Mexico',
'MHL': 'Marshall Islands',
'MKD': 'North Macedonia',
'MLI': 'Mali',
'MLT': 'Malta',
'MMR': 'Myanmar',
'MNE': 'Montenegro',
'MNG': 'Mongolia',
'MNP': 'Northern Mariana Islands',
'MOZ': 'Mozambique',
'MRT': 'Mauritania',
'MSR': 'Montserrat',
'MTQ': 'Martinique',
'MUS': 'Mauritius',
'MWI': 'Malawi',
'MYS': 'Malaysia',
'MYT': 'Mayotte',
'NAM': 'Namibia',
'NCL': 'New Caledonia',
'NER': 'Niger',
'NFK': 'Norfolk Island',
'NGA': 'Nigeria',
'NIC': 'Nicaragua',
'NIU': 'Niue',
'NLD': 'Netherlands',
'NOR': 'Norway',
'NPL': 'Nepal',
'NRU': 'Nauru',
'NZL': 'New Zealand',
'OMN': 'Oman',
'PAK': 'Pakistan',
'PAN': 'Panama',
'PCN': 'Pitcairn Islands',
'PER': 'Peru',
'PHL': 'Philippines',
'PLW': 'Palau',
'PNG': 'Papua New Guinea',
'POL': 'Poland',
'PRI': 'Puerto Rico',
'PRK': 'North Korea',
'PRT': 'Portugal',
'PRY': 'Paraguay',
'PSE': 'State of Palestine',
'PYF': 'French Polynesia',
'QAT': 'Qatar',
'REU': 'Réunion',
'ROU': 'Romania',
'RUS': 'Russia',
'RWA': 'Rwanda',
'SAU': 'Saudi Arabia',
'SDN': 'Sudan',
'SEN': 'Senegal',
'SGP': 'Singapore',
'SGS': 'South Georgia and the South Sandwich Islands',
'SHN': 'Saint Helena, Ascension and Tristan da Cunha',
'SJM': 'Svalbard and Jan Mayen',
'SLB': 'Solomon Islands',
'SLE': 'Sierra Leone',
'SLV': 'El Salvador',
'SMR': 'San Marino',
'SOM': 'Somalia',
'SPM': 'Saint Pierre and Miquelon',
'SRB': 'Serbia',
'SSD': 'South Sudan',
'STP': 'São Tomé and Príncipe',
'SUR': 'Suriname',
'SVK': 'Slovakia',
'SVN': 'Slovenia',
'SWE': 'Sweden',
'SWZ': 'Eswatini',
'SXM': 'Sint Maarten',
'SYC': 'Seychelles',
'SYR': 'Syria',
'TCA': 'Turks and Caicos Islands',
'TCD': 'Chad',
'TGO': 'Togo',
'THA': 'Thailand',
'TJK': 'Tajikistan',
'TKL': 'Tokelau',
'TKM': 'Turkmenistan',
'TLS': 'East Timor',
'TON': 'Tonga',
'TTO': 'Trinidad and Tobago',
'TUN': 'Tunisia',
'TUR': 'Turkey',
'TUV': 'Tuvalu',
'TWN': 'Taiwan',
'TZA': 'Tanzania',
'UGA': 'Uganda',
'UKR': 'Ukraine',
'UMI': 'United States Minor Outlying Islands',
'URY': 'Uruguay',
'USA': 'United States',
'UZB': 'Uzbekistan',
'VAT': 'Vatican City',
'VCT': 'Saint Vincent and the Grenadines',
'VEN': 'Venezuela',
'VGB': 'British Virgin Islands',
'VIR': 'United States Virgin Islands',
'VNM': 'Vietnam',
'VUT': 'Vanuatu',
'WLF': 'Wallis and Futuna',
'WSM': 'Samoa',
'YEM': 'Yemen',
'ZAF': 'South Africa',
'ZMB': 'Zambia',
'ZWE': 'Zimbabwe',
}

country_projects = ['WikiProject ' + v for v in list(set(countries.values()))]


f = open('outmid.newregex', 'r')
wikiprojects = json.loads(f.read())
f.close()

#for w in wikiprojects['wikiprojects']:
#	print(w)
#exit()

print(
'''<html><head><title>Results</title><script src='https://unpkg.com/context-cards/dist/context-cards.js'></script><style>table, th, td { border: 1px solid black; }</style></head><meta charset='UTF-8'><body>
<p>Predictions in <span style="font-weight:bold; color:orange">bold orange</span> differ from the highest probability drafttopic prediction. Sometimes they match the second or third highest probability drafttopic prediction, sometimes they've been looked up directly based on UGC, sometimes other heuristics are used.</p>
<p>Key:</p>
<ul>
<li><b>page title x (Talk):</b> page title and talk page. Note you can hover on the page title and clicks on either link will open in a new tab.</li>
<li><b>predicted:</b> predicted (sometimes renamed) topic after the heuristics are applied</li>
<li><b>is_human:</b> strong indicator the subject is human, based on [[Category]] mappings</li>
<li><b>has_geo:</b> the article bears geocoordinates according to MariaDB geo_tags table</li>
<li><b>has_list:</b> strong indication this is a list page based on wikiproject or title</li>
<li><b>country_association:</b> heuristically derived country associated with this article based on {{Infobox settlement}} or in some other string mapping for a wikiproject or the title. Notice this could be further tuned (e.g., for synonyms or territories within a country), but it it matches on obvious things for now.</li>
<li><b>topic:</b> from the talk page of the article, the highest signal wikiproject as inferred from the UGC (usually the wikiproject first listed with the highest importance assignment amongst the wikiprojects denoted)</li>
<li><b>topic_first_encountered:</b> from the talk page of the article, the first encountered wikiproject, which can be useful if the other wikiprojects don't turn out to match machine predictions neatly or there were no significant importance assignments</li>
<li><b>best1:</b> drafttopic's highest scoring topic assignment</li>
<li><b>best1_score:</b> drafttopic's estimated probability for the highest scoring topic assignment</li>
</ul>
<table>
''')
#print("<p>The 'predicted' column is a refinement that tries for (a) subjects that apparently refer to people to identify the non-geography subject matter most interesting about the people; it specifically de-prioritizes the 'Culture.Language and literature' which is biography-linked until proven otherwise, as that's generally a given in a metadata sense about such topics, and (b) after accounting for the matter in (a) for subjects without geocoordinate information embedded in the article tries to identify the non-geography subject matter most interesting about the subject (unless the geographic linkage via a drafttopic prediction exceeds a high threshold.</p>")
#print("<p>Key:</p><h1><u>UGC's wikiproject with 'highest rating'  agreed with a top-3 drafttopic prediction</u><h1><h1>UGC's first listed wikiproject agreed with a top-3 drafttopic prediction</h1><h2><u>UGC's wikiproject with 'highest rating' not found in drafttopic, but found in mid-level categories anyway</u></h2><h2>UGCs' first listed wikiproject not found in drafttopic, but found in mid-level categories anyway</h2><h3>A drafttopic result looked okay enough</h3><p>(Unstyled) We exhausted our options and we're taking just the most highly rated drafttopic prediction</p>")
rows = 0;

with open('sample10000.tsv') as tsv:
	for line in tsv:
		parts = line.split("\t")
		title = parts[2]
		#print("<tr><td><a href='https://en.wikipedia.org/wiki/" + ul.quote(title) + "' data-wiki-lang='en' data-wiki-title='" + ul.quote(title) + "'>" + title.replace("_", " ") + "</a> (<a href='https://en.wikipedia.org/wiki/Talk:" + ul.quote(title) + "'>T</a>)</td>")

		print("<tr><td><a target='_blank' href='https://en.wikipedia.org/wiki/" + ul.quote(title) + "' data-wiki-lang='en' data-wiki-title='" + ul.quote(title) + "'>" + title.replace("_", " ") + "</a> (<a target='_blank' href='https://en.wikipedia.org/wiki/Talk:" + ul.quote(title) + "'>Talk</a>)<br /><br /><br /></td>")
		
		predicted, is_human, has_geo, has_list, country_association = ['predicted'] + parts[7:9] + ['has_list'] + ['country_association']
		topic, topic_rating, topic_first_encountered, topic_first_encountered_rating, best1, best1_score, best2, best2_score, best3, best3_score, title_y, page_id_ns_0, infobox_name, country, division_granularity, country_direct  = parts[11:]

		topic = topic.replace('WikiProject Elections and Referendums', 'WikiProject Elections and Referenda')
		topic_first_encountered = topic_first_encountered.replace('WikiProject Elections and Referendums', 'WikiProject Elections and Referenda')





#	page_id	page_title_x	rev_id	pageviews	page_title_y	page_latest	is_human	has_geo	title_x	page_id_ns_1	topic	topic_rating	topic_first_encountered	topic_first_encountered_rating	best1	best1_score	best2	best2_score	best3	best3_score	title_y	page_id_ns_0	infobox_name	country	division_granularity	country_direct
#1560071	50348800.0	List_of_Stop!!_Hibari-kun!_episodes	881813158.0	126	List_of_Stop!!_Hibari-kun!_episodes	881813158.0			List_of_Stop!!_Hibari-kun!_episodes	50348805	WikiProject Anime and manga	low	WikiProject Lists	unknown_importance	Culture.Entertainment	0.645384686292839	Culture.Broadcasting	0.5083503476220342	Culture.Visual arts	0.4170614440031028



		# this part has a bug. i don't want best1 to be picked up if there was a lower best that fit
		if rows > 0:
			if topic == 'WikiProject Disambiguation' or topic_first_encountered == 'WikiProject Disambiguation' or '(disambiguation)' in title.lower():
				predicted = 'Disambiguation'


			if topic == 'WikiProject Lists' or topic_first_encountered == 'WikiProject Lists' or title.startswith('List_of_'):

				has_list = '1.0'
				# predicted = '<h1><i>LISTS!</i></h1>'
			else:
				has_list = ''

			country = country.strip()
			if country.startswith('UNKNOWN'):
				country = ''
			country_direct = country_direct.strip()
			if country_direct.startswith('UNKNOWN'):
				country_direct = ''
			if country or country_direct:
				country_association = country if country else country_direct
				predicted = country_association
			elif topic in country_projects:
				country_association = topic.replace('WikiProject ', '')
			else:
				country_association = ''

			if predicted == 'predicted':
				for b in [best1, best2, best3]:
					if 'Wikipedia:' + topic in wikiprojects['wikiprojects'][b]:
						if topic == 'WikiProject Lists' or (has_list and b == 'Culture.Language and literature'):
							continue
						if b.startswith('Assistance'):
							continue
						if topic == 'WikiProject Biography' and b == 'Culture.Language and literature':
							continue
						if (is_human or topic == 'WikiProject Biography' or not has_geo) and b.startswith('Geography'):
							continue
						if b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps']:
							continue
						predicted = b
						break

			if predicted == 'predicted':
				for b in [best1, best2, best3]:
					if 'Wikipedia:' + topic_first_encountered in wikiprojects['wikiprojects'][b]:
						if topic_first_encountered  == 'WikiProject Lists' or (has_list and b == 'Culture.Language and literature'):
							continue

						if b.startswith('Assistance'):
							continue
						if topic_first_encountered == 'WikiProject Biography' and b == 'Culture.Language and literature':
							continue

						if (is_human or topic_first_encountered == 'WikiProject Biography' or not has_geo) and b.startswith('Geography'):
							continue
						if b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps']:
							continue
						predicted = b
						break


			if predicted == 'predicted':
				for wikiproject in wikiprojects['wikiprojects']:
					if 'Wikipedia:' + topic in wikiprojects['wikiprojects'][wikiproject]:
						if topic == 'WikiProject Lists':
							continue

						if wikiproject.startswith('Assistance'):
							continue

						if topic == 'WikiProject Biography' and wikiproject  == 'Culture.Language and literature':
							continue

						if (is_human or topic == 'WikiProject Biography' or not has_geo) and wikiproject.startswith('Geography'):
							continue
						if wikiproject.startswith('Geography') and wikiproject not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps']:
							continue
						predicted = wikiproject
						break


			if predicted == 'predicted':
				for wikiproject in wikiprojects['wikiprojects']:
					if 'Wikipedia:' + topic_first_encountered in wikiprojects['wikiprojects'][wikiproject]:

						if topic_first_encountered == 'WikiProject Lists':
							continue

						if wikiproject.startswith('Assistance'):
							continue

						if topic_first_encountered == 'WikiProject Biography' and wikiproject  == 'Culture.Language and literature':
							continue

						if (is_human or topic_first_encountered == 'WikiProject Biography' or not has_geo) and wikiproject.startswith('Geography'):
							continue
						if wikiproject.startswith('Geography') and wikiproject not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps']:
							continue
						predicted = wikiproject
						break


			if predicted == 'predicted':
				for b, b_score in [(best1, best1_score), (best2, best2_score), (best3, best3_score)]:
					score = float(b_score)

					if b == 'Culture.Language and literature' or b.startswith('Assistance'):
						continue

					if (is_human or topic == 'WikiProject Biography' or topic_first_encountered == 'WikiProject Biography') and b.startswith('Geography') and b != 'Geography.Maps':
						continue

					if b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps'] and country_association and score >= 0.95 and has_geo:
						predicted = country_association
						break

					if not has_geo and b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps']:
						continue

					if b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps'] and score < 0.95:
						continue

					if score > 0.14:
						predicted = b
						break


			# TODO: consider avoiding geo category if lacking coordinates.
			# Notice how Utricularia kimberleyensis really ought to be STEM.Biology, which is 2nd ORES result
			# Likewise notice how XHMI-FM should probably be Culture.Broadcasting although it's MX radio

			# TODO: resolve Women Scientists. Notice how Karen Wynn shows up under Culture.Language and literature because of WikiProject Women Scientists moniker.


			if predicted == 'predicted':
				for b in [best1, best2, best3]:
					if b.startswith('Assistance'):
						continue
					elif has_geo and country_association and b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps']:
						predicted = country_association
						break
					elif ('WikiProject Biography' in [topic, topic_first_encountered] or is_human) and (country_association or (b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps'])):
						predicted = 'Regional society (best guess)'
						break
			if predicted == 'predicted':
				for b in [best1, best2, best3]:
					if b.startswith('Assistance'):
						continue
					elif b.startswith('Geography') and b not in ['Geography.Bodies of water', 'Geography.Landforms', 'Geography.Maps']:
						predicted = 'Regional geography (best guess)'
						break
					elif country_association:
						predicted = 'Regional interest (best guess)'
					else:
						predicted = b + ' (best guess)'
						break

		bold_it = False
		if predicted != best1:
			bold_it = True

		taxons = predicted.split(".")
		if len(taxons) > 1:
			predicted = taxons[1]
		predicted = predicted.replace("Plastic arts", "Structures of note")

		if bold_it:
			predicted = '<div style="font-weight:bold; color:orange">' + predicted + '</div>'

		for p in [predicted, is_human, has_geo, has_list, country_association, topic, topic_first_encountered, best1, best1_score]:
			print("<td>" + p + "</td>")
		
		print("</tr>")
		rows += 1
print("</table></body></html>")
