import random

class EmbeddingService:
    def __init__(self, dim: int):
        self.dim = dim

    def generate(self, text: str):
        random.seed(hash(text) % (10**9))
        return [random.random() for _ in range(self.dim)]
