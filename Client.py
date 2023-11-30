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


class ClientSolver:
    SERVER_AD = ""

    def __init__(self, code: str):
        self.hash = code
        self.need_work = True
        self.socket = None
        self.segments_needed = cpu_count()
        self.threads = []
        for cpu in range(cpu_count()):
            temp_obj = HashSolver
            self.threads.append(temp_obj)
            temp_thread = threading.Thread(target=temp_obj.check_range)
            temp_thread.start()

    def connect(self):
        """Connects to the server with a socket
           sets the socket as self.socket
           """
        pass

    def get_work(self):
        """Get a segment for each thread that doesn't have a segment"""
        # Connect to server



    """Still need to finish the client class: need to write the "get_work" func
                                              need to write "assign_work" func
                                              connect function
       Need to write the server class
    """
