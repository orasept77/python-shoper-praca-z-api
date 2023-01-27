import requests

from shoperapi import ShoperClient


#s = requests.Session()
#response = s.post('https://sklep853310.shoparena.pl/webapi/rest/auth', auth=("python_api", "Gangam77"))
#print(response.json())
#result = response.json()
#token = result['access_token']
#s.headers.update({'Authorization': 'Bearer %s' % token})




from shoperapi import ShoperClient

URL = "https://sklep853310.shoparena.pl/webapi/rest"

client = ShoperClient(URL, "python_api", "Gangam77", access_token='xxxxxxxxxxxxxxxxxxxxx')
client.get_user_token()

#URL = "https://rogaz.shoparena.pl/webapi/rest"

#client = ShoperClient(URL, "python_api", "Gangam77", access_token='ef81841f8c4f0ae7276e5114e2f4bca7dda6b14e')

#client.get_user_token()


#{'access_token': 'ef81841f8c4f0ae7276e5114e2f4bca7dda6b14e', 'expires_in': 2592000, 'token_type': 'bearer'}

#URL = "https://rogaz.shoparena.pl/webapi/rest"
#client = ShoperClient(URL, "python_api", "Gangam77")
#client.get_user_token()