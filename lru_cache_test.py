from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        value = self.cache.pop(key)
        self.cache[key] = value
        return value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

# teste da implementação:
if __name__ == "__main__":
    lru = LRUCache(3)
    lru.put(1, 100)
    lru.put(2, 200)
    lru.put(3, 300)
    print(lru.get(1))  # Deve imprimir 100
    lru.put(4, 400)    # Remove o elemento menos recente (chave 2)
    print(lru.get(2))  # Deve imprimir -1 (não encontrado)
