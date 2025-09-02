#circular linked list = regular linked list that continues to first from last
class Task:
    def __init__(self, id, cycles_left):
        #initializing
        self.id = id
        self.cycles_left = cycles_left
        self.next = self
        self.prev = self
    def reduce_cycles(self, n):
        #decreasing cycles_left by n
        self.cycles_left -= n

class TaskQueue:
    def __init__(self, cycles_per_task = 1):
        #initializing
        self.current = None
        self.cycles_per_task = cycles_per_task
        self.len = 0
        self.tasks = [None] * 256
        av_id = []
        for i in range (255):
            av_id.append(i)
        
    def add_task(self, t):
        #change so you cannot choose you id#######, make it return an id
        #override the id of the task you are adding

        #take previous node make it the current one
        if t.id > 255 or t.id < 0:
           # we can reallocate a larger array if we need more than 255 tasks running at the same time
           raise RuntimeError("id " + str(t.id) + " must be in [0,255]")
        if self.tasks[t.id]:
           raise RuntimeError("Task id " + str(t.id) + " already exists and is still running")
        self.tasks[t.id] = t
        if (self.current==None):
            self.current = t
        else:
            t.prev = self.current.prev
            t.next = self.current
            self.current.prev = t
            t.prev.next = t
        #increase length
        self.len += 1

    def find_node(self, id):
    	return self.tasks[id]
            
    def remove_task(self, id):        
        t = self.find_node(id)
        if (t == None):
            raise RuntimeError("id " + str(id) + " not in TaskQueue")
            #return None
        #changing the reference so they access the correct node
        t.next.prev = t.prev 
        t.prev.next = t.next
        self.tasks[id] = None
        
        #decreasing len by 1
        self.len -= 1

    def is_empty(self):
        #check if length is zero
        return (self.len == 0)

    def get_available_id(self):
        #pop the first id
        #after push the id back in
        pass

    def execute_tasks(self):
        cycle_count = 0
        while (self.len > 0):
            #check if any cycles left
            if (self.cycles_per_task <= self.current.cycles_left):
                self.current.cycles_left -= self.cycles_per_task #this is the execution
                cycle_count += self.cycles_per_task #counting how many cycles used
            else:
                cycle_count += self.cycles_per_task #counting cycles if theres more cycles per task than cycles left
                self.current.cycles_left = 0
            if (self.current.cycles_left <= 0):
                id = self.current.id
                self.current = self.current.next
                self.remove_task(id)
                print (f"removed {id}")
            else:
                self.current = self.current.next
        return cycle_count