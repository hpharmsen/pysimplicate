import time
import requests


class Simplicate:
    def __init__(self, subdomain, api_key, api_secret):
        self.subdomain = subdomain
        self.api_key = api_key
        self.api_secret = api_secret

    from ._crm import organisation, persons
    from ._employee import employees
    from ._hours import hours_types, hours_count, hours_data, hours_data_simplified, turnover
    from ._hrm import leave, leave_simplified, leavetypes, leavebalance
    from ._invoices import invoices
    from ._projects import projects, service, purchasetypes
    from ._sales import revenue_groups
    from ._service import defaultservices

    def call(self, url_path: str):
        my_headers = {'Authentication-Key': self.api_key, 'Authentication-Secret': self.api_secret}
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        url = self.add_url_param(url, 'metadata', 'count')
        url = self.add_url_param(url, 'offset', '')
        result = []
        offset = 0
        connection_reset_tries = 0
        while True:
            try:
                url2 = url + str(offset)
                while True:
                    response = requests.get(url2, headers=my_headers, timeout=15)
                    if response.status_code == 429:
                        time.sleep(10)  # Rate limit exceeded. Wait 10 secs and try again
                        continue
                    break
                response.raise_for_status()
                # Code here will only run if the request is successful
                json = response.json()
                result += json['data']
                offset += 100
                if offset < json['metadata']['count']:
                    continue
                return result
            except requests.exceptions.HTTPError as errh:
                print(errh)
            except requests.exceptions.ConnectionError as errc:
                connection_reset_tries += 1
                if connection_reset_tries <= 2:
                    continue  # Try again
                print(errc)
            except requests.exceptions.Timeout as errt:
                connection_reset_tries += 1
                if connection_reset_tries <= 2:
                    continue  # Try again
                print(errt)
            except requests.exceptions.RequestException as err:
                print(err)
            print(url2)
            try:
                print(response.content)
            except:
                pass  # There was no respons yet
            return False

    def add_url_param(self, url, key, value):
        delimiter = '&' if url.count('?') else '?'
        return url + delimiter + key + '=' + requests.utils.quote(value)
