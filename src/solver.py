from ast import excepthandler
from http import client
import math
import random
from copy import deepcopy


def distance(p1, p2):
    if not p1 or not p2:
        return 0
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def rindex(k):
    return random.randint(0,k-1)

def shallow_copy(routes):
    copy = { rid : route.copy() for rid, route in routes.items() }
    return copy

def shallow_copy2(routes):
    copy = { a : b for a,b in routes.items() }

class Solver:
    def __init__(self, clients_loc, clients_demand, routes, max_capacity, depot) -> None:
        # problema specification fields
        self.clients_loc = clients_loc
        self.clients_demand = clients_demand
        self.max_capacity = max_capacity
        self.depot = depot
        
        # solution specification fields
        self.routes = routes
        self.routes_cost = {}
        self.routes_capacity = {}
        for idr, route in self.routes.items():
            self.routes_cost[idr] = self.compute_route_cost(route)
            self.routes_capacity[idr] = self.compute_route_capacity(route)

        self.current_route = -1
        self.selected_clients = []
        self.operations = []
        self.backup = None
        self.not_valid = False
    
    def backup_solution(self):
        self.routes_backup = shallow_copy(self.routes)
        self.routes_cost_backup = self.routes_cost.copy()
        self.routes_capacity_backup = self.routes_capacity.copy()
    
    def load_backup(self):
        self.not_valid=False
        self.routes = shallow_copy(self.routes_backup)
        self.routes_cost = self.routes_cost_backup.copy()
        self.routes_capacity = self.routes_capacity_backup.copy()


    def register_operation(self, op):
        self.operations.append(op)
    
    def reset(self):
        self.operations = []

    def compute_solution(self):
        self.not_valid = False
        self.selected_clients = []
        for op in self.operations:
            try:
                op()
            except:
                self.not_valid = True
                return

    def compute_route_cost(self, route):
        cost = 0
        if not route:
            return 0
        for i in range(1, len(route)):
            c1 = route[i]
            c2 = route[i-1]
            cost += distance(self.clients_loc[c1], self.clients_loc[c2])
        return cost + distance(self.clients_loc[route[0]], self.depot) + distance(self.clients_loc[route[len(route)-1]], self.depot)

    def compute_route_capacity(self, route):
        capacity = self.max_capacity
        for c in route:
            capacity -= self.clients_demand[c]
        return capacity
    
    def add_client_to_route(self, idr, idc, index=None):
        # print(f"adding clinet {idc} to route {idr} at index {index}")
        route = self.routes[idr]
        if index is None or index > len(route):
            index = len(route)-1
        route.insert(index+1, idc)

        self.routes_capacity[idr] -= self.clients_demand[idc]

    # Route selection operation and filters

    def select_route_random(self):
        self.current_route = random.choice(list(self.routes.keys()))

    def select_route_not_empty(self):
        self.current_route = random.choice(list(rid for rid in self.routes if self.routes[rid]))

    def select_route_min_cost(self):
        self.current_route = sorted(self.routes_cost.items(), key=lambda x: x[1])[0][0]
    
    def select_route_max_cost(self):
        self.current_route = sorted(self.routes_cost.items(), key=lambda x: x[1], reverse=True)[0][0]
    
    def select_route_min_capacity(self):
        self.current_route = sorted(self.routes_capacity.items(), key=lambda x: x[1])[0][0]

    def select_route_max_capacity(self):
        self.current_route = sorted(self.routes_capacity.items(), key=lambda x: x[1], reverse=True)[0][0]

    # Client selection operations

    def select_random_client(self):
        self.remove_client_from_route()

    def select_minimize_cost_client(self):
        route = self.routes[self.current_route]
        best_cost = float('inf')
        best_index = None
        for i, idc in enumerate(route):
            prev = self.clients_loc[route[i-1]] if i > 0 else self.depot
            next = self.clients_loc[route[i+1]] if i < len(route) - 1 else self.depot
            new_cost = self.routes_cost[self.current_route]
            new_cost -= distance(prev, self.clients_loc[idc]) + distance(self.clients_loc[idc], next)
            new_cost += distance(prev, next)
            best_cost = min(best_cost, new_cost)
            if best_cost == new_cost:
                best_index = i
        self.remove_client_from_route(best_index)
    

    def remove_client_from_route(self, index=None):
        route = self.routes[self.current_route]
        if not route:
            return

        if not index or index > len(route):
            index = rindex(len(route))
            
        client = route.pop(index)
        self.routes_capacity[self.current_route] += self.clients_demand[client]

        self.selected_clients.append((client, self.current_route, index))
    
    def exchange_clients(self):
        client1, route1, index1 = self.selected_clients.pop(rindex(len(self.selected_clients)))
        client2, route2, index2 = self.selected_clients.pop(rindex(len(self.selected_clients)))
        self.add_client_to_route(route1, client2, index1)
        self.add_client_to_route(route2, client1, index2)

    def insert_random_client(self):
        rid = random.choice(list(self.routes.keys()))
        client, route, index = self.selected_clients.pop(rindex(len(self.selected_clients)))
        self.add_client_to_route(rid, client)
    
    def insert_feasible_client(self):
        client, route, index = self.selected_clients.pop(rindex(len(self.selected_clients)))
        rid = random.choice(list(idr for idr in self.routes if self.routes_capacity[idr] > self.clients_demand[client]))
        self.add_client_to_route(rid, client)
    
    def solution_cost(self):
        if self.not_valid:
            return 100000000000000

        if sum(len(route) for route in self.routes.values()) < 32:
            print(True)
            return 1000000000000000

        if all(capacity >= 0 for capacity in self.routes_capacity.values()):
            s = 0
            for idr, route in self.routes.items():
                cost = self.compute_route_cost(route)
                self.routes_cost[idr] = cost
                s += cost
            return s
        else:
            return 100000000000000

    



    




