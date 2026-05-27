import sys

class HashTable:
    def __init__(self, initial_capacity=1):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [[] for _ in range(self.capacity)]

    def _get_bucket(self, key):
        key_hash = hash(key)
        index = key_hash & (self.capacity - 1) 
        return self.buckets[index]

    def _resize(self, new_capacity):
       
        new_buckets = [[] for _ in range(new_capacity)]
        
        for bucket in self.buckets:# Rehash and move existing elements to the new buckets
            for key, value in bucket:
                key_hash = hash(key)
                index = key_hash & (new_capacity - 1) # bitwise AND for fast indexing
                new_buckets[index].append([key, value])
        
        self.capacity = new_capacity
        self.buckets = new_buckets

    def insert(self, key, value): # Resize 
        bucket = self._get_bucket(key)
        
        for i in range(len(bucket)): # Update value if the key already exists
            if bucket[i][0] == key:
                bucket[i][1] = value
                return
                
        bucket.append([key, value]) # Append as a new entry if the key is not found

        self.size += 1

        if self.size >= self.capacity:
            self._resize(self.capacity * 2) # Double the capacity 

    def search(self, key):
        bucket = self._get_bucket(key)
        
        for k, v in bucket: # Search for the key in the specific bucket
            if k == key:
                return v
        return None

    def delete(self, key):
        bucket = self._get_bucket(key)
        
        for i in range(len(bucket)):# Find and delete the key-value pair
            if bucket[i][0] == key:
                bucket.pop(i)
                self.size -= 1
                
                if self.capacity > 1 and self.size <= self.capacity // 4:
                    self._resize(self.capacity // 2)
                    
                return

    def items(self):
      
        for bucket in self.buckets:  
            for key, value in bucket:
                yield key, value