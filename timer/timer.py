from sys import stdout
from time import sleep

def timer(duration_sec: int):
    seconds_per_unit = duration_sec / 60
    for i in range(61):
        stdout.write(
            f"\r[{ '#'*i + '.'*(60-i) }] | {i*seconds_per_unit:.1f}/{duration_sec}"
        )
        stdout.flush()
        sleep(seconds_per_unit)
    stdout.write("\n")
