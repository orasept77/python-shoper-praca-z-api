import requests

from shoperapi import ShoperClient


#s = requests.Session()
#response = s.post('https://sklep853310.shoparena.pl/webapi/rest/auth', auth=("", ""))
#print(response.json())
#result = response.json()
#token = result['access_token']
#s.headers.update({'Authorization': 'Bearer %s' % token})




from shoperapi import ShoperClient

URL = "https://sklep853310.shoparena.pl/webapi/rest"

client = ShoperClient(URL, "", "", access_token='xxxxxxxxxxxxxxxxxxxxx')
client.get_user_token()

#URL = "https://rogaz.shoparena.pl/webapi/rest"

#client = ShoperClient(URL, "", "", access_token='')

#client.get_user_token()


#{'access_token': '', 'expires_in': 2592000, 'token_type': 'bearer'}

#URL = "https://rogaz.shoparena.pl/webapi/rest"
#client = ShoperClient(URL, "", "")
#client.get_user_token()
