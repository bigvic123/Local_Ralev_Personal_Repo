# See assignment for class attributes.
# Remember to include docstrings.
# Start with unittests

class LocalRecord:
    def __init__(self, pos, max=None, min=None, precision = 0):
        '''initializing variables'''
        self.pos = pos
        self.max = max
        self.min = min

    def add_report(self, temp):
        '''Changing max/min temp if necessary'''
        #setting a new temp if it is higher than max
        if self.max is None or self.max < temp:
            self.max = temp
            #setting a new temp if it is smaller than min
        if self.min is None or self.min > temp:
            self.min = temp

    def __eq__(self, other):
        '''Return if positions are equal'''
        return int(round(self.pos[0], 0))==int(round(other.pos[0], 0)) and int(round(self.pos[1], 0))==int(round(other.pos[1], 0))

    def __hash__(self): 
        '''Returns the custom hash given position'''
        return abs(int(round(self.pos[0], 0)))*100+abs(int(round(self.pos[1], 0)))
        
    def __repr__(self):
        '''Represent as a string'''
        return f"Record(pos={self.pos}, max={self.max}, min={self.min}"


class RecordsMap:
    def __init__(self, size=256):
        '''Initializing hashtable with size 256'''
        self.ha = [[] for g in range(size)]
        self.cnt = 0

    def __len__(self):
        '''Calculating length of all items in the hash table'''
        return self.cnt

    def add_report(self, pos, temp):
        '''Adding a new weather report to the hash table'''
        #create report
        rep = LocalRecord(pos)
        #find hash
        n = hash(rep) % len(self.ha)
        #add into the correct hash
        for rec in self.ha[n]:
            if rec.pos == pos:
                rec.add_report(temp)
                return
        # we couldn't find rep in the list
        rep.add_report(temp)
        self.ha[n].append(rep)
        self.cnt += 1
        # check if we need to rehash
        bucket_cnt = len(self.ha)
        r = len(self)/bucket_cnt
        if r > 0.75:
            self._rehash(bucket_cnt*2)

    def get_local_rec(self, pos):
        '''Getting a weather report from the position'''
        #create report
        rep = LocalRecord(pos)
        size = len(self.ha)
        #find hash
        n = hash(rep) % size
        #return min and max at correct position
        for rec in self.ha[n]:
            if rec.pos == pos:
                return [rec.min, rec.max]
        return None
         
    def __getitem__(self, pos):
        '''Find position, return if it exists'''
        minmax = self.get_local_rec(pos)
        if minmax:
            return minmax
        #if minmax doesn't exist raise keyerror
        raise KeyError(f"Position={pos} is not in the map")

    def __contains__(self, pos):
        '''If position exists, then return true'''
        if self.get_local_rec(pos):
            return True
        else:
            return False

    def _rehash(self, m_new):
        '''Rehash to decrease load factor'''
        #create new hash array
        new_ha = [[] for h in range(m_new)]
        #propperly store values in new hash array
        for recs in self.ha:
            for rec in recs:
                new_ha[hash(rec) % m_new].append(rec)
        self.ha = new_ha

    def num_buckets(self):
        return len(self.ha)