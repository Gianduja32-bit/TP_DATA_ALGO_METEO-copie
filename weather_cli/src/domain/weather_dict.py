class WeatherDictionary:
    
    def __init__(self, size: int = 10):
        self.size = size
        self.buckets = [[] for _ in range(size)]
        self._count = 0
    
    def _hash(self, key: str) -> int:

        return hash(key) % self.size
    
    def set(self, key: str, value) -> None:
        index = self._hash(key)
        
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                self.buckets[index][i] = (key, value)
                return
        
        self.buckets[index].append((key, value))
        self._count += 1
    
    def get(self, key: str):
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return None
    
    def delete(self, key: str) -> bool:
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                del self.buckets[index][i]
                self._count -= 1
                return True
        return False
    
    def contains(self, key: str) -> bool:

        return self.get(key) is not None
    
    def keys(self) -> list[str]:
        all_keys = []
        for bucket in self.buckets:
            for k, v in bucket:
                all_keys.append(k)
        return all_keys
    
    def values(self) -> list:

        all_values = []
        for bucket in self.buckets:
            for k, v in bucket:
                all_values.append(v)
        return all_values
    
    def __len__(self) -> int:
        return self._count
    
    def __str__(self) -> str:
        items = []
        for bucket in self.buckets:
            for k, v in bucket:
                items.append(f"{k}: {v}")
        return "{" + ", ".join(items) + "}"
