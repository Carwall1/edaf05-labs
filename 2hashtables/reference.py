import sys
from separate_chaining import HashTable

d = HashTable()

i = 0

for line in sys.stdin:
    word = line.strip()
    
    current_count = d.search(word)
    is_present = current_count is not None
    
    remove_it = i % 16 == 0

    if is_present:
        if remove_it:
            d.delete(word)
        else:
            d.insert(word, current_count + 1)
    elif not remove_it:
        d.insert(word, 1)
    i += 1

keys = [k for k, v in d.items()]
values = [v for k, v in d.items()]
(count, word) = max(zip(values, keys))

for k, v in d.items():
    if v == count and k < word:
        word = k

print(word, count)