import psutil
import signal
import sys

terminate = False

def signal_handler(sig, frame):
    global terminate
    terminate = True

signal.signal(signal.SIGINT, signal_handler)

cpus = []
while not terminate:
    cpu = psutil.cpu_percent(interval=1)
    cpus.append(cpu)
print(sum(cpus)/len(cpus))
