from http import client
import math
import random


def distance(p1, p2):
    if not p1 or not p2:
        return 0
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def rindex(k):
    return random.randint(0,k-1)

class Solver:
    def __init__(self, clients_loc, clients_demand, routes, max_capacity) -> None:
        # problema specification fields
        self.clients_loc = clients_loc
        self.clients_demand = clients_demand
        self.max_capacity = max_capacity
        
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

    def register_operation(self, op):
        self.operations.append(op)
    
    def reset(self):
        self.operations = []

    def compute_solution(self):
        for op in self.operations:
            op()

    def compute_route_cost(self, route):
        cost = 0
        for i in range(1, len(route)):
            c1 = route[i]
            c2 = route[i-1]
            cost += distance(self.clients_loc[c1], self.clients_loc[c2])
        return cost

    def compute_route_capacity(self, route):
        capacity = self.max_capacity
        for c in route:
            capacity -= self.clients_demand[c]
        return capacity
    
    def add_client_to_route(self, idr, idc, index=None):
        route = self.routes[idr]
        index = index if index else len(route)
        prev = route[index-1] if index > 0 else None
        next = route[index+1] if index < len(route) - 1 else None
        route.insert(idc, index+1)
        self.routes_cost[idr] += distance(self.clients_loc[prev], self.clients_loc[idc])
        self.routes_cost[idr] += distance(self.clients_loc[idc], self.clients_loc[next])
        self.routes_capacity[idr] -= self.clients_demand[idc]

    # Route selection operation and filters

    def select_route_random(self):
        self.current_route = random.choice(list(self.routes.keys()))

    def select_route_not_empty(self):
        self.current_route = random.choice(list(rid for rid in self.routes if self.routes[rid]))

    def select_route_min_cost(self):
        self.current_route = sorted(self.routes_cost.items(), lambda x: x[1])[0][0]
    
    def select_route_max_cost(self):
        self.current_route = sorted(self.routes_cost.items(), lambda x: x[1], reverse=True)[0][0]
    
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
            prev = route[i-1] if i > 0 else None
            next = route[i+1] if i < len(route) - 1 else None
            new_cost = self.routes_cost[self.current_route]
            new_cost -= distance(self.clients_loc[prev], self.clients_loc[idc]) + distance(self.clients_loc[idc], self.clients_loc[next])
            new_cost += distance(self.clients_loc[prev], self.clients_loc[next])
            best_cost = min(best_cost, new_cost)
            if best_cost == new_cost:
                best_index = i
        self.remove_client_from_route(best_index)
    

    def remove_client_from_route(self, index=None):
        route = self.routes[self.current_route]
        if not index:
            index = rindex(len(route))

        prev = index - 1 if index > 0 else None
        next = index + 1 if index < len(route) - 1 else None 
        client = route.pop(index)
        self.routes_cost[self.current_route] -= distance(self.clients_loc[prev], self.clients_loc[client]) + distance(self.clients_loc[client], self.clients_loc[next])
        self.routes_cost[self.current_route] += distance(self.clients_loc[prev], self.clients_loc[next])
        self.routes_capacity[self.current_route] += self.clients_demand[client]

        self.selected_clients.append((client, route, index))
    
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
    
    

    



    




