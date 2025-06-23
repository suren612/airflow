import json
import os
import psutil
import signal
import time

terminate = False

def signal_handler(sig, frame):
    global terminate
    terminate = True

signal.signal(signal.SIGINT, signal_handler)

disk = os.environ["DISK"]

iops_r = []
iops_w = []
iops = psutil.disk_io_counters(perdisk=True)
prev_r = iops[disk].read_count
prev_w = iops[disk].write_count

while not terminate:
    iops = psutil.disk_io_counters(perdisk=True)
    r = iops[disk].read_count - prev_r
    w = iops[disk].write_count - prev_w
    iops_r.append(r)
    iops_w.append(w)
    prev_r = iops[disk].read_count
    prev_w = iops[disk].write_count
    time.sleep(1)

res = {
    "read": sum(iops_r)/len(iops_r),
    "write": sum(iops_w)/len(iops_w)
}
print(json.dumps(res))
