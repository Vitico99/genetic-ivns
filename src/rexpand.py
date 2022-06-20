import visitor
from symbols import *
import random

class RExpandVisitor:

    @visitor.on('symbol')
    def visit(self, symbol, h):
        pass

    @visitor.when(TerminalSymbol)
    def visit(self, symbol: TerminalSymbol, h):
        pass
    
    @visitor.when(NonTerminalSymbol)
    def visit(self, symbol: NonTerminalSymbol, h):
        production = random.choice(symbol.productions)
        for s in production():
            symbol.add_child(s)
            self.visit(s, h)

    @visitor.when(S1Symbol)
    def visit(self, symbol: S1Symbol, h):
        if h > 0:
            production = random.choice(symbol.productions)
        else:
            production = symbol.p3
        
        for s in production():
            symbol.add_child(s)
            self.visit(s, h-1)

        

            



