import os
import pickle

def insecure_deserialization():
	f = open("demo.pickle","rb")
	na = pickle.load(f)
	return na
if __name__ == '__main__':
	print(insecure_deserialization())