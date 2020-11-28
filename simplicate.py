import requests
import settings

class Simplicate():
    def __init__(self):
        print( self.organisation() )

    def call(self, url_path):
        my_headers = {'Authentication-Key': settings.api_key,
                      'Authentication-Secret': settings.api_secret}
        url = f'https://{settings.subdomain}.simplicate.nl/api/v2{url_path}'
        try:
            response = requests.get(url, headers=my_headers, timeout=5)
            response.raise_for_status()
            # Code here will only run if the request is successful
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)
        return False

    def organisation(self):
        result = self.call( '/crm/organization')
        return result


    def projects(self):
        result = self.call( '/projects/project')
        return result