from collections import deque

def fifo_page_replacement(frames, pages):
    """Simulate FIFO page replacement algorithm."""
    memory = deque(maxlen=frames)  # Queue with fixed size
    page_faults = 0
    memory_states = []
    for page in pages:
        if page not in memory:
            if len(memory) == frames:
                memory.popleft()  # Remove oldest page
            memory.append(page)
            page_faults += 1
        memory_states.append(page_faults)
    return page_faults, memory_states

def lru_page_replacement(frames, pages):
    """Simulate LRU page replacement algorithm."""
    memory = []  # List to track page usage order
    page_faults = 0
    memory_states = []
    for page in pages:
        if page not in memory:
            if len(memory) == frames:
                memory.pop(0)  # Remove least recently used page
            memory.append(page)
            page_faults += 1
        else:
            memory.remove(page)  # Move page to end (most recently used)
            memory.append(page)
        memory_states.append(page_faults)
    return page_faults, memory_states

def optimal_page_replacement(frames, pages):
    """Simulate Optimal page replacement algorithm."""
    memory = []
    page_faults = 0
    memory_states = []
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                # Predict which page won't be used longest
                future_uses = [pages[i+1:].index(p) if p in pages[i+1:] else float('inf') for p in memory]
                page_to_replace = memory[future_uses.index(max(future_uses))]
                memory.remove(page_to_replace)
                memory.append(page)
            page_faults += 1
        memory_states.append(page_faults)
    return page_faults, memory_states