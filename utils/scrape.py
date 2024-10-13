import csv
import json
import re
import requests
import time
from email.message import Message

def download(url, session):
    for attempt in range(3):
        if attempt >= 1:
            print('Download failed; trying again')
        try:
            response = session.get(url)
            message = Message()
            message['content-disposition'] = response.headers['content-disposition']
            filename = message.get_filename()
            with open(filename, 'wb') as file:
                file.write(response.content)
            time.sleep(1)
        except Exception:
            pass
        else:
            break

session = requests.Session()
response = session.get('https://beta-naptan.dft.gov.uk/download/la')
match = re.search(r'const localAuthoritiesList = (.*);', response.text)
local_authorities = json.loads(match.group(1))
with open('local_authorities.csv', 'w', newline='') as csvfile:
    fieldnames = ['atcoCodePrefix', 'localAuthorityName']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for local_authority in local_authorities:
        local_authority_name = local_authority['localAuthorityName']
        atco_code_prefix = local_authority['atcoCodePrefix']
        match = re.search(r'(.*) \(\d{3}\)', local_authority['localAuthorityName'])
        local_authority['localAuthorityName'] = match.group(1)
        writer.writerow(local_authority)
        print(f'Downloading NaPTAN files for {local_authority_name}')
        for format in ('xml', 'csv'):
            download(f'https://naptan.api.dft.gov.uk/v1/access-nodes?atcoAreaCodes={atco_code_prefix}&dataFormat={format}', session)
print('Downloading NPTG files')
download('https://naptan.api.dft.gov.uk/v1/nptg', session)
download('https://naptan.api.dft.gov.uk/v1/nptg/localities', session)
