import time


class FullnessObject:
    is_full = False
    timestamp = time.time()

    def __init__(self, is_full):
        self.is_full = is_full
