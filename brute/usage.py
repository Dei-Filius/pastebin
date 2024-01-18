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
        result[1]
        == b"\xc0\x00H\xf3\xa4:\xfb\xa0c\xc1\x0e`\xdeY\xd7V\xb8&j\xd80\x0ej\x88\xd5\x93Og\xa1\x9f\x81L"
    ):
        return True
    return False


# this "if" is a must or else will error. idky
if __name__ == "__main__":
    print(brute.run(64, gen_data, worker, result_checker))
