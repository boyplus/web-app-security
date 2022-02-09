import os
import pickle
import base64

def serialize_exploit():
	obj = {"name": "Thanaphon"}
	res = base64.b64encode(pickle.dumps(obj)).decode()
	print(res)

if __name__ == '__main__':
	serialize_exploit()