import json
import re
import requests
from email.message import Message

session = requests.Session()
response = session.get('https://beta-naptan.dft.gov.uk/download/la')
match = re.search('const localAuthoritiesList = (.*);', response.text)
local_authorities = json.loads(match.group(1))
for local_authority in local_authorities:
    atco_code_prefix = local_authority['atcoCodePrefix']
    for format in ('xml', 'csv'):
        response = session.get(f'https://naptan.api.dft.gov.uk/v1/access-nodes?atcoAreaCodes={atco_code_prefix}&dataFormat={format}')
        message = Message()
        message['content-disposition'] = response.headers['content-disposition']
        filename = message.get_filename()
        with open(filename, 'wb') as file:
            file.write(response.content)
