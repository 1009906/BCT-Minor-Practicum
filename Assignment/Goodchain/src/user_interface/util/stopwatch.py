import time

class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def get_elapsed_time(self):
        if self.end_time == None: 
            return time.time() - self.start_time
        return self.end_time - self.start_time

    def print_elapsed_time(self):
        print(f"Elapsed time: {self.get_elapsed_time()} seconds")