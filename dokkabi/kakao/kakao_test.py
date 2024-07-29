import requests

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = 'f6216629fd1ef75a0e3daa8512912a93'
redirect_uri = 'https://example.com/oauth'
authorize_code = 'xF0qD88aBD2PACQKJR8uLAx_96BXpruxgu6T4ifXF4bl-mM-cXPxzQAAAAQKKiUQAAABkI3vGVjRDLJpR7eCqA'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# json 저장
import json
#1.
with open(r"C:\macro\kakao_code.json","w") as fp:
    json.dump(tokens, fp)