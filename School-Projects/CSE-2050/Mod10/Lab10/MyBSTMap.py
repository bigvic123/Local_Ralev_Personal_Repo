class Entry:
    def __init__(self, item, priority):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
      return self.item == other.item and self.priority == other.priority
        

class PQ_UL:
  def __init__(self):
    self._L = []
    
  def __len__(self):
    return len(self._L)        

  def insert(self, item, priority):
    self._L.append(Entry(item, priority))
    
  def find_min(self):
    return min(self._L)

  def remove_min(self):
    entry = min(self._L)
    self._L.remove(entry)
    return entry


class PQ_OL:
  def __init__(self):
    self._L = []

  def __len__(self):
    return len(self._L)
        
  def insert(self, item, priority):
    self._L.append(Entry(item, priority))
    self._L.sort(reverse = True)

  def find_min(self):
    return self._L[-1]

  def remove_min(self):
    return self._L.pop()