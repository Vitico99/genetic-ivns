from symbols import *
from rexpand import RExpandVisitor
from printer import PrinterVisitor

rexpand = RExpandVisitor()
printer  = PrinterVisitor()
s = SSymbol()
rexpand.visit(s, 4)
printer.visit(s)
print(printer.string)