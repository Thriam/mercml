import time
import random
from datetime import datetime

while True:
    with open("data/stream/censor.csv", "a") as f:
        temp = round(random.uniform(20, 40), 2)
        f.write(f"{datetime.now()},{temp}\n")
    time.sleep(1)