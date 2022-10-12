"""
Implement a class called LoadBalancer that has the following methods.
Add_server:  add server ID to an available pool. We can assume that ID is always UNIQUE
Remove_server: remove server ID from the available pool
Pick_server: randomly pick a server ID with the same probability of other available servers being selected.
For example, if there are servers = 1,2,3,4,5, the method may return 1 with 20% probability.
class LoadBalancer
 # takes ID of server, and add the ID to the available servers pool
 def add_server(id)
    pass

 # takes ID of a server, and removes the server from the servers pool
 # return true, if the ID exists
 # return false, if the ID doesn't exist
 def remove_server(id)
    pass

 # Randomlay pick ID of server with same probablity in respect to other servers.
 # at fist, we don't need to worry about if the server is being used. As long as the server is added, the ID of the server can be picked.
 # return the ID, if there exists available server
 # return null, there is no server
 def pick_server

Test:
add_server 5
add_server 2
remove_server 1
add_server 1
remove_server 1
add_server 3
Pick_server => return any of 5 ,2 and 3
add_server 4
Pick_server => return any ay of 5 ,2 , 3 and 4
"""

import random


class LoadBalancer(object):
    def __init__(self):
        self.pool = []
        self.id_index = {}

    def add_server(self, id):
        self.pool.append(id)
        self.id_index[id] = len(self.pool) - 1
        self.print_pool()

    def remove_server(self, id):
        if id in self.pool:
            self.pool.remove(id)
            return True
        else:
            return False

    def pick_server(self):
        if len(self.pool) == 0:
            return None
        return random.choice(self.pool)

    def print_pool(self):
        print(f"Pool => {self.pool}")


lb = LoadBalancer()

lb.add_server(id=5)
lb.add_server(id=2)
lb.remove_server(id=1)
lb.add_server(id=1)
lb.remove_server(id=1)
lb.add_server(id=3)
print(lb.pick_server())
lb.add_server(id=4)
print(lb.pick_server())
