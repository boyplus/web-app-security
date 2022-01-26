
# encoded = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDMxNDQ0MzYsIm5iZiI6MTY0MzE0NDQzNiwianRpIjoiNzQ0MjQ0OWMtZWY3OC00MTRlLTlhNzAtMDk0ZWJjMjg0NGM0IiwiZXhwIjo4ODA0MzE0NDQzNiwiaWRlbnRpdHkiOjIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.oGhLGrCqRHFmVpFplxpVUiMTtmreL_rBq8RaHhgm0yU"
# dec = jwt.decode(encoded, key, algorithms="HS256")
# print(dec)

# encoded = jwt.encode({}, key, algorithm="HS256")


import jwt
key = "secret-key"
payload_data = {
	'iat': 1643144436,
	'nbf': 1643144436,
	'jti': '7442449c-ef78-414e-9a70-094ebc2844c4', 
	'exp': 88043144436,
	'identity': 1, 
	'fresh': False, 
	'type': 'access',
	'was': True
}

token = jwt.encode(
    payload=payload_data,
    key=key,
    algorithm="HS256"
)
print(token)

