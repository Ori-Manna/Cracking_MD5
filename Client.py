from os import cpu_count
import hashlib
import threading
import time
import logging
import socket


class HashSolver:
    WAITING_FOR_WORK = 1
    WORK = 2
    FOUND = 3

    def __init__(self, code: str, code_len: int):
        self.code = code
        self.code_len = code_len
        self.start_range = None
        self.end_range = None
        self.state = HashSolver.WAITING_FOR_WORK
        self.result = None

    def update_range(self, num_range: tuple):
        self.start_range = num_range[0]
        self.end_range = num_range[1]
        self.state = HashSolver.WORK

    def check_num(self, num) -> bool:
        num = str(num).zfill(self.code_len)
        result = hashlib.md5(num.encode()).hexdigest()
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


class ClientSolver:
    SERVER_AD = "172.16.14.33"
    PORT = 8820

    def __init__(self):
        self.found = False
        self.hash = None
        self.code_len = None
        self.socket = socket.socket()
        self.segments_needed = cpu_count()
        self.solvers = []

    def connect(self) -> bool:
        try:
            self.socket.connect((self.SERVER_AD, self.PORT))
        except:
            return False
        return True

    def get_code(self):
        self.socket.send("CODE".encode())
        response = self.socket.recv(1024).decode()
        self.hash, _, self.code_len = response.partition(":")

    def create_solvers(self):
        for cpu in range(cpu_count()):
            temp_obj = HashSolver(self.hash, self.code_len)
            self.solvers.append(temp_obj)
            temp_thread = threading.Thread(target=temp_obj.check_range)
            temp_thread.start()

    def get_work_from_server(self):
        """Get a segment for each thread that doesn't have a segment"""
        self.socket.send(str(self.segments_needed).encode())
        segments = self.socket.recv(1024).decode()
        if segments == "DONE":
            self.found = True
        else:
            segments = segments.split(",")
            for seg in segments:
                for solver in self.solvers:
                    if solver.state == HashSolver.WAITING_FOR_WORK:
                        solver.update_range(seg)

        self.segments_needed = 0

    def work(self):
        need_work = False
        while not self.found:
            repeat_look_for_work = False

            for solver in self.solvers:
                if solver.state == HashSolver.WAITING_FOR_WORK:
                    self.segments_needed += 1
                    need_work = True
                    repeat_look_for_work = True
                elif solver.state == HashSolver.FOUND:
                    self.found = True
                    self.socket.send(f"FOUND:{solver.result}")
                    break

            if need_work and (not repeat_look_for_work):
                self.get_work_from_server()
                need_work = False

    def end_work(self):
        for solver in self.solvers:
            solver.state = HashSolver.FOUND

    """
    need to make a "Start_up" func for client
    
       Need to write the server class
    writing to and from the server class:
    what to respond with to each message the server gets:
    - a number: respond with an amount of segments equal to the number, separated by ',' (NO SPACE)
    - "CODE": the hash code, followed by ':', followed by the code length
    
    When the solver finds the result, he will send "FOUND:" followed by the number (SAME MESSAGE, NO SPACE)
    If a different solver found the number, next time the solver asks for work the server needs to respond with "DONE"
    
    
    """
