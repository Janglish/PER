import random

class SegTree:
    
    def __init__(self, n_, seed=None):
        
        self.n = 1
        while self.n < n_: self.n *= 2
        self.data = [0 for _ in range(self.n * 2 - 1)]
        random.seed(seed)
        
    def __str__(self):
        
        return str(self.data[self.n - 1:])
        
    def __setitem__(self, idx, val):
        
        idx += self.n - 1
        self.data[idx] = val
        
        while idx > 0:
            idx = (idx - 1) // 2
            self.data[idx] = self.data[idx * 2 + 1] + self.data[idx * 2 + 2]

    def __getitem__(self, idx):
        
        idx += self.n - 1
        return self.data[idx]
        
    def sample(self, val=None):
        
        val = random.uniform(0, self.data[0]) if val is None else val
        
        idx = 0
        while idx < self.n - 1:

            idx_l = 2 * idx + 1
            idx_r = 2 * idx + 2

            if val > self.data[idx_l]:
                idx = idx_r
                val -= self.data[idx_l]
            else:
                idx = idx_l
        
        idx -= self.n - 1
        return idx