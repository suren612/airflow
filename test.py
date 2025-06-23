import datetime
import os
import time

print("Sleeping for 2 seconds")
time.sleep(2)
print(f"Current time: {datetime.datetime.now()}")
for k in os.environ:
    print(f"{k}={os.environ[k]}")
