import json
import time
import requests


class Simplicate:
    def __init__(self, subdomain, api_key, api_secret):
        self.subdomain = subdomain
        self.api_key = api_key
        self.api_secret = api_secret

    from ._crm import organisation, person
    from ._employee import employee
    from ._hours import hourstype, hourstype_simple, hours, hours_simple, hours_count, turnover, book_hours, hours_approval
    from ._hrm import contract, leave, leave_simple, leavetype, leavebalance
    from ._invoices import invoice, invoice_per_year
    from ._projects import project, project_by_name, projectstatus, projectstatus_dict, service, purchasetypes
    from ._sales import revenuegroup, revenuegroup_dict, sales, sales_flat
    from ._service import defaultservice

    def call(self, url_path: str):
        my_headers = {'Authentication-Key': self.api_key, 'Authentication-Secret': self.api_secret}
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        delimiter = '&' if url.count('?') else '?'
        url += delimiter + 'metadata=count&offset='
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

    def post(self, url_path: str, post_fields: dict):
        headers = {
            'Authentication-Key': self.api_key,
            'Authentication-Secret': self.api_secret,
            'Content-type': 'application/json',
            'Accept': 'text/plain',
        }
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        response = requests.post(url, json=post_fields, headers=headers)
        return response

    def add_url_param(self, url, key, value, operator=''):
        # Adds parameter to the simplicate API url in the form: &q[key]=value or &q[key][operator]=value
        delimiter = '&' if url.count('?') else '?'
        operator = f'[{operator}]' if operator else ''
        return url + delimiter + f'q[{key}]' + operator + '=' + requests.utils.quote(str(value))

    def check_filter(self, function_name, fields, filter):
        # Checks if the keys in the passed filter are all supported by the function
        unused_keys = [k for k in filter.keys() if k not in fields]
        assert (
            not unused_keys
        ), f'parameter(s) {unused_keys} not supported by function {function_name}. Supported fields are {tuple(fields.keys())}'
