from ctypes import c_char_p
from multiprocessing import Manager, Pool, Process, RLock, Value, active_children
from os import getpid, kill
from signal import CTRL_C_EVENT, SIG_IGN, SIGINT, signal, SIGTERM, SIGBREAK
from threading import Event, RLock
from typing import Callable

from tqdm import tqdm
from time import sleep



# validate the user inputs into brute()
def validate(
    instances: int, gen_data: Callable, worker: Callable, result_checker: Callable
):
    ...


def warlord(
    num: int,
    lock: RLock,
    pool_size: int,
    data: tuple | list,
    worker: Callable,
    result_checker: Callable,
    is_found: Event,
    out,
):
    tqdm.set_lock(lock)
    with Pool(pool_size, signal, (SIGINT, SIG_IGN)) as pool:
        try:
            with tqdm(
                total=len(data),
                position=num,
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}]",
                leave=False,
            ) as bar:
                try:
                    for result in pool.imap_unordered(worker, data):
                        if not is_found.is_set():
                            bar.update()
                            halt = result_checker(result)
                            if halt:
                                out.value = result[0]
                                is_found.set()
                                break
                            # break
                            # raise KeyboardInterrupt
                        else:
                            # bar.close()
                            # pool.terminate()
                            # pool.join()
                            # # return
                            # raise KeyboardInterrupt
                            break

                except KeyboardInterrupt:
                    bar.close()
                    # bar.close()
                    # pool.terminate()
                    # pool.join()
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            # pool.close()
            # print(f"[warlord {num}] KeyboardInterrupt")
    # except KeyboardInterrupt:
    #     # print(f"[warlord {num}] KeyboardInterrupt")
    #     pass
    # for child in active_children():
    #     child.terminate()


def run(instances: int, gen_data: Callable, worker: Callable, result_checker: Callable):
    validate(instances, gen_data, worker, result_checker)
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
            result_checker,
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
            result_checker,
            is_found,
            out,
        ]
        p = Process(target=warlord, args=args)
        lords.append(p)

    print("Let's begin")

    for lord in lords:
        lord.start()

    try:
        # for lord in lords:
        #     lord.join()

        # sleep(5)
        # kill(0, CTRL_C_EVENT)

        is_found.wait()

        for lord in lords:
            print("joining", lord.pid)
            lord.join()

        # return out.value
        # raise KeyboardInterrupt

        # for lord in lords:
        #     if lord.is_alive():
        #         kill(lord.pid, CTRL_C_EVENT)

        # lord.join()
        # sleep(30)

        while True:
            print("fyaksjfhskjdhfksjdhf" + out.value)
            print(out.value)

        # for lord in active_children():
        #     lord.terminate()
        #     lord.join()

        # print("[main] is found", flush=True)
        # kill(0, CTRL_C_EVENT)

        # for lord in lords:
        #     kill(lord.pid, CTRL_C_EVENT)
        #     lord.join()
        #     print("lord", lord.pid)
        # sleep(10)
        # print(getattr(out, "value"))

        # for num, lord in enumerate(lords, 1):
        #     if lord.pid is not None:
        #         print("kill")
        #         kill(lord.pid, CTRL_C_EVENT)

        # for num, lord in enumerate(lords, 1):
        #     print(lord.pid)
        #     if lord.is_alive():
        #         kill(lord.pid, CTRL_C_EVENT)
        #     else:
        #         lord.terminate()

        # is_found.wait()
        # for lord in lords:
        #     lord.terminate()
        #     lord.join()
        # print(getattr(out, "value", None))
        # # print(out.value)

        # for num, lord in enumerate(lords, 1):
        #     # lord.terminate()
        #     lord.join()
        #     # print(num, lord.is_alive())
        #     print(f"[warlord {num}]: stopped")
        #     print(1, getattr(out, "value"))
        # print("[main] warlords joined f")
        # print(2, getattr(out, "value"))

    except KeyboardInterrupt:
        print(
            "akfsjddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddhjdhskjdhfks"
        )
        # for child in active_children():
        #     child.terminate()
        #     child.join()
        for num, lord in enumerate(lords, 1):
            # if lord.is_alive():
            # #     kill(lord.pid, CTRL_C_EVENT)
            #     lord.terminate()
            lord.join()
            print(f"[warlord {num}]: stopped", flush=True)
        print("tf", getattr(out, "value", None))
        print("[main] warlords joined due to KeyboardInterrupt", flush=True)

    return getattr(out, "value", None)


if __name__ == "__main__":
    print("import as module")
