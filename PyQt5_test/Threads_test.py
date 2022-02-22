import time
import threading
import serial
import io

start = time.perf_counter()

def do_something ():
    while(1):
        print("Sleeping 2 second....")
        time.sleep(2)
        print("Done Sleeping....")

t1 =threading.Thread(target = do_something)
t1.start()

t1.join()

finish = time.perf_counter()

print(f'Finished in {abs(round(start-finish,2))} seconds(s)')



