from mailbox import linesep
from pickletools import floatnl
from sys import float_info
from unittest import result
from build_criteria import CriteriaVisitor
from solver import Solver
from symbols import *
from rexpand import RExpandVisitor
from printer import PrinterVisitor
import json

problem = {}
clients_loc = None
clients_demand = None
routes = None

with open('src/A-n33-k6', 'r') as f:
    problem = json.load(f)

clients_loc = { int(c) : loc for c, loc in problem['clients_loc'].items() }
clients_demand = {int(c) : demand for c, demand in problem['clients_demand'].items() }
max_capacity = problem['capacity']
routes = {int(v) : route for v, route in problem['basic_solution'].items() } 
depot = problem['depot']

clients_loc.setdefault(0, None)
clients_demand.setdefault(0, None)

solver = Solver(clients_loc, clients_demand, routes, max_capacity, depot)
cvisitor = CriteriaVisitor(solver)
rexpand = RExpandVisitor()

k = 0
a = 0
d = 0
solver.backup_solution()
results = {}
while a < 100000:
    s = SSymbol()
    rexpand.visit(s, 7)
    cvisitor.visit(s) 
    a += 1
    d = 0
    while a < 100000 and d < 4:
        current_cost = solver.solution_cost()
        results[current_cost] = True
        solver.compute_solution()
        new_cost = solver.solution_cost()
        if new_cost > current_cost:
            solver.load_backup()
            break
        else:
            solver.backup_solution()
        d += 1
print(f'Vecindades generadas {a}')
print(f'Mínimo hallado: {solver.solution_cost()}')
