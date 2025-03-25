from collections import deque

class FIFOHandler:
    def __init__(self, frames):
        self.memory = deque(maxlen=frames)
        self.page_faults = 0

    def step(self, page):
        if page not in self.memory:
            self.memory.append(page)
            self.page_faults += 1
        return self.page_faults, list(self.memory)

class LRUHandler:
    def __init__(self, frames):
        self.memory = []
        self.page_faults = 0
        self.frames = frames

    def step(self, page):
        if page not in self.memory:
            if len(self.memory) == self.frames:
                self.memory.pop(0)
            self.memory.append(page)
            self.page_faults += 1
        else:
            self.memory.remove(page)
            self.memory.append(page)
        return self.page_faults, list(self.memory)

class OptimalHandler:
    def __init__(self, frames, full_sequence):
        self.memory = []
        self.page_faults = 0
        self.frames = frames
        self.full_sequence = full_sequence
        self.current_step = 0

    def step(self, page):
        if page not in self.memory:
            if len(self.memory) < self.frames:
                self.memory.append(page)
            else:
                future_uses = []
                for p in self.memory:
                    try:
                        idx = self.full_sequence[self.current_step+1:].index(p)
                        future_uses.append(idx)
                    except ValueError:
                        future_uses.append(float('inf'))
                page_to_replace = self.memory[future_uses.index(max(future_uses))]
                self.memory.remove(page_to_replace)
                self.memory.append(page)
            self.page_faults += 1
        self.current_step += 1
        return self.page_faults, list(self.memory)

# Original functions for compatibility
def fifo_page_replacement(frames, pages):
    handler = FIFOHandler(frames)
    for page in pages:
        handler.step(page)
    return handler.page_faults

def lru_page_replacement(frames, pages):
    handler = LRUHandler(frames)
    for page in pages:
        handler.step(page)
    return handler.page_faults

def optimal_page_replacement(frames, pages):
    handler = OptimalHandler(frames, pages)
    for page in pages:
        handler.step(page)
    return handler.page_faults