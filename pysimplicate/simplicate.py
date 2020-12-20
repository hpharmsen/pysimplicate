import time

import requests

class Simplicate():
    def __init__(self, subdomain, api_key, api_secret):
        self.subdomain = subdomain
        self.api_key = api_key
        self.api_secret = api_secret

    def call(self, url_path: str):
        my_headers = {'Authentication-Key': self.api_key,
                      'Authentication-Secret': self.api_secret}
        url = f'https://{ self.subdomain}.simplicate.nl/api/v2{url_path}'
        url = add_url_param(url, 'metadata', 'count')
        url = add_url_param(url, 'offset', '')
        result = []
        offset = 0
        connection_reset_tries = 0
        while True:
            try:
                url2 = url + str(offset)
                while True:
                    response = requests.get(url2, headers=my_headers, timeout=15)
                    if response.status_code == 429:
                        time.sleep(10) # Rate limit exceeded. Wait 10 secs and try again
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
                connection_reset_tries +=1
                if connection_reset_tries <= 2:
                    continue # Try again
                print(errc)
            except requests.exceptions.Timeout as errt:
                connection_reset_tries +=1
                if connection_reset_tries <= 2:
                    continue # Try again
                print(errt)
            except requests.exceptions.RequestException as err:
                print(err)
            print(url2)
            try:
                print(response.content)
            except:
                pass # There was no respons yet
            return False

    def organisation(self):
        result = self.call( '/crm/organization')
        return result


    def projects(self, from_date:str='', until_date:str='' ,status:str=''):
        url = '/projects/project?sort=-updated_at'
        if from_date:
            url += '&q[modified][ge]='+from_date
        if until_date:
            url += '&q[created][le]='+until_date
        if status: #!! Dit werkt niet helaas. URL is '/projects/project?sort=-updated_at&q[modified][ge]=2019-01-01&q[created][le]=2019-07-01&q[project_status.label]=tab_pactive'
            assert status in ('active', 'closed'), "Status can only be 'active' or 'closed'"
            url += '&q[project_status.label]=tab_p' + status
        result = self.call(url)
        return result

    def hours_types(self):
        url = '/hours/hourstype'
        result = self.call(url)
        return {d['id']:{'type':d['type'], 'tariff':d['tariff'], 'label':d['label']} for d in result}

    def hours_data(self, project:str=None, service:str=None, label:str=None, revenue_group_id:str=None,
                   hourstype:str=None, employee:str=None,
                   from_date:str= '', until_date:str= ''):
        url = '/hours/hours?sort=start_date'
        if project:
            url += '&q[project.project_number]=' + project
        if service:
            url += '&q[projectservice.name]=' + service
        if label:
            url += '&q[type.label]=' + label
        if revenue_group_id:
            url += '&q[projectservice.revenue_group_id]=' + revenue_group_id
        if hourstype:
            url += '&q[type.label]=' + hourstype
        if employee:
            url += '&q[employee.name]=' + employee
        if from_date:
            url += '&q[start_date][ge]=' + from_date
        if until_date:
            url += '&q[start_date][le]=' + until_date
        result = self.call(url)
        return result

    def hours_data_simplified(self, project:str=None, service:str=None, label:str=None, revenue_group_id:str=None,
                              hourstype:str=None, employee:str=None, from_date:str= '', until_date:str= ''):
        data = self.hours_data( project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
        result = [{'employee':d['employee']['name'],
                   'project_name':d['project']['name'],
                   'project_number':d['project']['project_number'],
                   'service':d['projectservice']['name'],
                   'type':d['type']['type'],
                   'label':d['type']['label'],
                   'billable':d['billable'],
                   'tariff':d['tariff'],
                   'hours':d['hours'],
                   'start_date':d['start_date'],
                   'status':d['status'],
                   'corrections':d['corrections']
                   } for d in data]
        return result

    def hours_count(self, project:str=None, service:str=None, label:str=None, revenue_group_id:str=None,
                    hourstype:str=None, employee:str=None, from_date:str= '', until_date:str= ''):
        hours = self.hours_data(project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
        # todo: Correcties eraf trekken
        return sum([d['hours'] for d in hours])

    def turnover(self, project:str=None, service:str=None, label:str=None, revenue_group_id:str=None,
                 hourstype:str=None, employee:str=None, from_date:str= '', until_date:str= ''):
        hours = self.hours_data(project, service, label, revenue_group_id, hourstype, employee, from_date, until_date)
        # todo:  Correcties eraf trekken
        if not hours:
            #print( 'Could not calculate hours', locals())
            return 0
        for h in hours:
            if h['corrections']['amount'] > 0:
                corrections = h['corrections']['amount']
                corrections += 0

        return sum([d['hours']*d['tariff'] for d in hours])

    def invoices(self, from_date:str='', until_date:str='', year=''):
        from_date_str, until_date_str = date_param( **locals() )
        url = '/invoices/invoice?sort=id'
        if from_date_str:
           url += '&q[date][ge]='+from_date
        if until_date_str:
            url += '&q[date][le]='+until_date
        result = self.call(url)
        return result

    def service(self):
        url = '/projects/service'
        result = self.call(url)
        return result

    # Diensten
    def defaultservices(self):
        url = '/services/defaultservice'
        result = self.call(url)
        return result

    # Omzetgroepen
    def revenue_groups(self):
        url = '/sales/revenuegroup'
        result = self.call(url)
        return result

    # Kostensoorten
    def purchasetypes(self):
        url = '/projects/purchasetype'
        result = self.call(url)
        return result

    def persons(self, first_name:str='', last_name:str=''):
        url = '/crm/person'
        if first_name:
            url = add_url_param( url, 'q[first_name]', first_name)
        if last_name:
           add_url_param( url, 'q[last_name]', last_name)
        result = self.call(url)
        return result


    def employees(self, first_name: str = '', last_name: str = '', active:bool=True):
        url = '/hrm/employee' #?name[gt]=&[status.label]=active
        if active:
            url = add_url_param(url, 'employment_status', 'active')
        if first_name:
            url = add_url_param(url, 'q[first_name]', first_name)
        if last_name:
            add_url_param(url, 'q[last_name]', last_name)
        result = self.call(url)
        return result


def date_param( **kwargs ):
    year = kwargs.get('year')
    from_date_str = kwargs.get('from_date_str')
    until_date_str = kwargs.get('until_date_str')
    assert year == '' or (from_date_str == '' and until_date_str == ''), \
        "you cannot specifiy both year and one of from_date_str and until_date_str"
    if year:
        return f'{year}-01-01', f'{year}-12-31'
    else:
        return from_date_str, until_date_str

def add_url_param( url, key, value):
    delimiter = '&' if url.count('?') else '?'
    return url + delimiter + key + '=' + value