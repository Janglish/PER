import zlib
import torch
import pickle
import random
import numpy as np
from SegTree import SegTree
from collections import namedtuple, deque

class ReplayBuffer:
    
    def __init__(self, capacity, gamma, Transition, epsilon, alpha, beta, device, seed):
        self.Transition = Transition
        self.capacity = capacity
        self.gamma = gamma
        self.buffer = []
        self.priorities = SegTree(n_=capacity, seed=seed)
        self.epsilon = epsilon
        self.alpha = alpha
        self.beta = beta
        self.min_priority = np.inf
        self.max_weight = -np.inf
        self.position = 0
        self.device = device
    
    def push(self, args, priority):
        
        if len(self.buffer) < self.capacity:
            self.buffer.append(None)
        
        experience = self.Transition(*args)
        experience = zlib.compress(pickle.dumps(experience))
        self.buffer[self.position] = experience
        self.priorities[self.position] = (abs(priority) + self.epsilon) ** self.alpha
        self.position = (self.position + 1) % self.capacity
        
    def sample(self, batch_size, steps_done, total_steps):
        indices = [self.priorities.sample() for _ in range(batch_size)]
        #indices = np.random.choice(np.arange(len(self.buffer)), replace=False, size=batch_size)
        experiences = tuple(pickle.loads(zlib.decompress(self.buffer[idx])) for idx in indices)
        beta = self.beta + (1 - self.beta) * steps_done / total_steps
        N = len(self.buffer)
        weights = torch.cat([torch.tensor([(N * (self.priorities[idx] / self.priorities.data[0])) ** (-beta)]) 
                             for idx in indices]).to(self.device)
        weights /= weights.max()
        return experiences, weights, indices
    
    def __len__(self):
        return len(self.buffer)