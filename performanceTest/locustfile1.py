import requests

data = {'email':'', 'password':''}
res = requests.post(url='', data=data)
print(res.json())