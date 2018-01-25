import heapq

class PriorityQueue:
    def __init__(self):
        self.elements=[]

    def empty(self):
        return len(self.elements)==0

    #in our case priority will be cost
    def put(self,node,priority):
        heapq.heappush(self.elements,(priority,node))


    def get(self):
        return heapq.heappop(self.elements)[1]