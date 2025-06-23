import base64
import datetime
import os
import time

print("Sleeping for 2 seconds")
time.sleep(2)
print(f"Current time: {datetime.datetime.now()}")
for k in os.environ:
    if k == "PARENT_STDOUTS":
        b64 = os.environ[k]
        utf8 = base64.b64decode(b64)
        print(f"{k}={utf8.decode('utf-8')}")
    print(f"{k}={os.environ[k]}")
