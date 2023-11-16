import hashlib
import math
import random
import threading
import time
import logging


def print_hex_encoding(num: int):
    if type(num) is not str:
        num = str(num)
    result_str = hashlib.md5(num.encode())
    print(f"The encoding of the string {num} is : {result_str.hexdigest()}")


class HashSolver:
    WAITING_FOR_WORK = 1
    WORK = 2
    FOUND = 3

    def __init__(self, code: str):
        self.code = code
        self.start_range = None
        self.end_range = None
        self.state = HashSolver.WAITING_FOR_WORK
        self.result = None

    def update_range(self, num_range: tuple):
        self.start_range = num_range[0]
        self.end_range = num_range[1]
        self.state = HashSolver.WORK

    def check_num(self, num) -> bool:
        result = hashlib.md5(str(num).encode()).hexdigest()
        logging.debug(f"The encoding of {num} is : {result}")
        if result == self.code:
            return True
        return False

    def check_range(self):
        while self.state != HashSolver.FOUND:
            while self.state == HashSolver.WAITING_FOR_WORK:
                time.sleep(0.01)

            if self.state == HashSolver.WORK:
                for i in range(self.start_range, self.end_range+1):
                    if self.check_num(i):
                        self.result = i
                        self.state = HashSolver.FOUND
                        break
                if self.state != HashSolver.FOUND:
                    self.state = HashSolver.WAITING_FOR_WORK


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] [%(asctime)s] (%(threadName)-10s) %(message)s')
    num_encoded = str(random.randint(0, 9)) + str(random.randint(0, 9))
    hashed_code = hashlib.md5(str(num_encoded).encode()).hexdigest()

    segments = []
    code_len = int(input("Code length: "))
    code_size = int(math.pow(10, code_len)) - 1
    seg_size = int(input("Segment length: "))
    num = 0
    while num <= code_size:
        if num + seg_size > code_size:
            segments.append((num, code_size))
        else:
            segments.append((num, num + seg_size - 1))
        num += seg_size

    threads = []

    thread_1_obj = HashSolver(hashed_code)
    threads.append(thread_1_obj)
    t_1 = threading.Thread(target=thread_1_obj.check_range)
    t_1.start()

    thread_2_obj = HashSolver(hashed_code)
    threads.append(thread_2_obj)
    t_2 = threading.Thread(target=thread_2_obj.check_range)
    t_2.start()

    result = None
    found = False
    while not found:
        for thread_obj in threads:
            if thread_obj.state == HashSolver.WAITING_FOR_WORK:
                thread_obj.update_range(segments[0])
                segments.pop(0)
            elif thread_obj.state == HashSolver.FOUND:
                found = True
                result = thread_obj.result

    for i in threads:
        i.state = HashSolver.FOUND

    print("Found the result!")
    print(f"The hash code was created from the number {num_encoded}, "
          f"and it resulted in the hash : {hashed_code}")
    print(f"The application found the hash was created from the number {result}")


if __name__ == '__main__':
    main()
