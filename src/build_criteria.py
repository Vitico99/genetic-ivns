import visitor
from symbols import *
from solver import Solver

class CriteriaVisitor():
    def __init__(self, solver: Solver) -> None:
        self.solver = solver

    @visitor.on('symbol')
    def visit(self, symbol):
        pass

    @visitor.when(rSymbol)
    def visit(self, symbol):
        self.solver.register_operation(self.solver.select_route_random)

    @visitor.when(aSymbol)
    def visit(self, symbol):
        self.solver.register_operation(self.solver.select_random_client)

    @visitor.when(bSymbol)
    def visit(self, symbol):
        self.solver.register_operation(self.solver.insert_random_client)
    
    @visitor.when(cSymbol)
    def visit(self, symbol):
        self.solver.register_operation(self.solver.exchange_clients)
    
    @visitor.when(frSymbol)
    def visit(self, symbol : frSymbol):
        if symbol.filter == 1:
            self.solver.register_operation(self.solver.select_route_min_cost)
        elif symbol.filter == 2:
            self.solver.register_operation(self.solver.select_route_max_cost)
        elif symbol.filter == 3:
            self.solver.register_operation(self.solver.select_route_min_capacity)
        elif symbol.filter == 4:
            self.solver.register_operation(self.solver.select_route_max_capacity)
        elif symbol.filter == 5:
            self.solver.register_operation(self.solver.select_route_not_empty)

    
    @visitor.when(faSymbol)
    def visit(self, symbol: faSymbol):
        if symbol.filter == 1:
            self.solver.register_operation(self.solver.select_minimize_cost_client)

    @visitor.when(fbSymbol)
    def visit(self, symbol: fbSymbol):
        if symbol.filter == 1:
            self.solver.register_operation(self.solver.insert_feasible_client)

    @visitor.when(SSymbol)
    def visit(self, symbol: SSymbol):
        self.solver.reset()
        for s in symbol.children:
            self.visit(s)
    
    @visitor.when(NonTerminalSymbol)
    def visit(self, symbol: NonTerminalSymbol):
        for s in symbol.children:
            self.visit(s)

    
        
