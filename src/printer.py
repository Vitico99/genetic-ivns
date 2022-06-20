import visitor
from symbols import *

class PrinterVisitor():
    def __init__(self) -> None:
        self.string = ''

    @visitor.on('symbol')
    def visit(self, symbol):
        pass

    @visitor.when(TerminalSymbol)
    def visit(self, symbol: TerminalSymbol):
        self.string += symbol.value
    
    @visitor.when(NonTerminalSymbol)
    def visit(self, symbol: NonTerminalSymbol):
        for s in symbol.children:
            self.visit(s)
    
    @visitor.when(SSymbol)
    def visit(self, symbol: SSymbol):
        self.string = ''
        for s in symbol.children:
            self.visit(s)