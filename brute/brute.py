from ctypes import c_char_p
from multiprocessing import Manager, Pool, Process, RLock, Value
from os import getpid, kill
from signal import CTRL_C_EVENT, SIG_IGN, SIGINT, signal, SIGTERM
from threading import Event, RLock
from typing import Callable

from tqdm import tqdm


# ignore. made for fun one
def timer(duration_sec: int):
    from sys import stdout
    from time import sleep

    seconds_per_unit = duration_sec / 60
    for i in range(61):
        stdout.write(
            f"\r[{ '#'*i + '.'*(60-i) }] | {i*seconds_per_unit:.1f}/{duration_sec}"
        )
        stdout.flush()
        sleep(seconds_per_unit)
    stdout.write("\n")


# validate the user inputs into brute()
def validate(
    instances: int, gen_data: Callable, worker: Callable, result_handler: Callable
):
    ...


def worker_init():
    signal(SIGINT, SIG_IGN)


def warlord_init():
    def handler(s, f):
        raise KeyboardInterrupt
    signal(SIGINT, handler)


def warlord(
    num: int,
    lock: RLock,
    pool_size: int,
    data: tuple | list,
    worker: Callable,
    result_handler: Callable,
    is_found: Event,
    out,
):
    # try:
    warlord_init()
    tqdm.set_lock(lock)
    with Pool(pool_size, worker_init) as pool:
        try:
            with tqdm(
                total=len(data),
                position=num,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]",
            ) as bar:
                bar.display()
                try:
                    for result in pool.imap_unordered(worker, data):
                        bar.update()
                        halt = result_handler(result)
                        if halt:
                            out.value = result
                            is_found.set()
                            raise KeyboardInterrupt
                except KeyboardInterrupt:
                    bar.clear()
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
                # print(f"[warlord {num}] KeyboardInterrupt")
    # except KeyboardInterrupt:
    #     # print(f"[warlord {num}] KeyboardInterrupt")
    #     pass
    print("past halt test", getattr(out, "value"))


def run(instances: int, gen_data: Callable, worker: Callable, result_handler: Callable):
    validate(instances, gen_data, worker, result_handler)
    print("pid:", getpid())

    WARRIORS = 60
    q = (instances + WARRIORS - 1) // WARRIORS
    print("instances:", instances)
    print("warlords:", q)

    print("running gen_data...")
    data: tuple = gen_data()
    pool_size = instances // q
    data_chunk = len(data) // q

    man = Manager()
    prlock = man.RLock()
    is_found = man.Event()
    out = Value(c_char_p)  # no lock, assume there is only 1 output

    lords: list[Process] = []
    for i in range(q - 1):
        num = i + 1
        print("creating warlord", num, flush=True)
        data_start = data_chunk * i
        data_end = data_start + data_chunk
        args = [
            num,
            prlock,
            pool_size,
            data[data_start:data_end],
            worker,
            result_handler,
            is_found,
            out,
        ]
        p = Process(target=warlord, args=args)
        lords.append(p)
    else:
        print("creating warlord", q)
        args = [
            q,
            prlock,
            pool_size + instances % q,
            data[data_chunk * (q - 1) :],
            worker,
            result_handler,
            is_found,
            out,
        ]
        p = Process(target=warlord, args=args)
        lords.append(p)

    print("Let's begin")
    try:
        for lord in lords:
            lord.start()

        is_found.wait()
        print("[main] is found")

        # for num, lord in enumerate(lords, 1):
        #     if lord.pid is not None:
        #         print("kill")
        #         kill(lord.pid, CTRL_C_EVENT)

        for num, lord in enumerate(lords, 1):
            print(lord.pid)
            if lord.is_alive():
                kill(lord.pid, CTRL_C_EVENT)
            else:
                lord.terminate()

    except KeyboardInterrupt:
        for num, lord in enumerate(lords, 1):
            lord.join()
            print(f"[warlord {num}]: stopped")
        print("[main] warlords joined")

    return getattr(out, "value")


if __name__ == "__main__":
    print("import as module")
