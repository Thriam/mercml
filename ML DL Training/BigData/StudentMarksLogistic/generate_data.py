import time
import random
from datetime import datetime
import os

os.makedirs("data/stream", exist_ok=True)

while True:
    temp = round(random.uniform(20, 40), 2)

    label = True if temp >= 30 else False

    with open("data/stream/censor.csv", "a") as f:
        f.write(f"{datetime.now()},{temp},{label}\n")

    time.sleep(1)
