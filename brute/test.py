import brute


# return tuple. elements are passed one by one into the worker function
def gen_data() -> tuple:
    return tuple(range(2**23, 2**24))


# input must correspoond with the gen_data function
# def worker(keys):
#     from Cryptodome.Cipher import AES

#     IV = bytes.fromhex("d8955dc3f209de63816d315cfe53a281")
#     CHOSEN = bytes.fromhex("74b838afa2a53bff3a2fd77c5c0b4022")  # input 0x00

#     a, b = keys
#     c1 = AES.new(a, AES.MODE_CBC, IV)
#     c2 = AES.new(b, AES.MODE_OFB, IV)
#     tmp = c1.decrypt((c2.decrypt(CHOSEN)))
#     return tmp, a, b


def worker(datum: int):
    from hashlib import sha256

    # output must be bytes for now. Future: do to do pickling
    return sha256(datum.to_bytes(3, "big")).digest()


# result handler must correspond with worker function's output
# Return True will halt the parallism and False means to continue
def result_checker(result):
    if (
        result
        == b'\x95\xb8-8\x99 \x0c\xfeK\x7fb\xb21\x9fxu\xd8\xdb\xfa -\xda\xb9,\xf9_\xa3\x06}\xf0\x8d\x95'
    ):
        return True
    return False


# this "if" is a must or else will error. idky
if __name__ == "__main__":
    print(brute.run(64, gen_data, worker, result_checker))
