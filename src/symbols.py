import random


class Symbol:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.is_terminal = False
        self.is_non_terminal = False

class TerminalSymbol(Symbol):
    def __init__(self, value) -> None:
        self.is_terminal = True
        self.value = value

class aSymbol(TerminalSymbol):
    def __init__(self) -> None:
        super().__init__('a')

class bSymbol(TerminalSymbol):
    def __init__(self) -> None:
        super().__init__('b')

class cSymbol(TerminalSymbol):
    def __init__(self) -> None:
        super().__init__('c')

class rSymbol(TerminalSymbol):
    def __init__(self) -> None:
        super().__init__('r')

class faSymbol(TerminalSymbol):
    def __init__(self) -> None:
        self.filter = 1
        super().__init__(f'[fa_{self.filter}]')

class fbSymbol(TerminalSymbol):
    def __init__(self) -> None:
        self.filter = 1
        super().__init__(f'[fb_{self.filter}]')

class frSymbol(TerminalSymbol):
    def __init__(self) -> None:
        self.filter = random.randint(1,5)
        super().__init__(f'[fr_{self.filter}]')

class foSymbol(TerminalSymbol):
    def __init__(self) -> None:
        self.filter = 1
        super().__init__(f'[fb_{self.filter}]')

class NonTerminalSymbol(Symbol):
    def __init__(self) -> None:
        self.is_non_terminal = True
        self.children = []
        self.productions = None
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

class SSymbol(NonTerminalSymbol):
    def __init__(self) -> None:
        super().__init__()
        self.productions = [self.p1, self.p2, self.p3, self.p4]
    
    def p1(self):
        return [RSymbol(), ASymbol(), S1Symbol(), BSymbol()]
    
    def p2(self):
        return [RSymbol(), ASymbol(), S1Symbol(), RSymbol(), BSymbol()]

    def p3(self):
        return [RSymbol(), ASymbol(), ASymbol(), S1Symbol(), CSymbol()]

    def p4(self):
        return [RSymbol(), ASymbol(), RSymbol(), ASymbol(), S1Symbol(), CSymbol()]


class S1Symbol(NonTerminalSymbol):
    def __init__(self) -> None:
        super().__init__()
        self.productions = [self.p1, self.p2, self.p3]

    def p1(self):
        return [R1Symbol(), ASymbol(), S1Symbol(), R1Symbol(), BSymbol()]
    
    def p2(self):
        return [R1Symbol(), ASymbol(), R1Symbol(), ASymbol(), S1Symbol(), CSymbol()]

    def p3(self):
        return []

class R1Symbol(NonTerminalSymbol):
    def __init__(self) -> None:
        super().__init__()
        self.productions = [self.p1, self.p2]

    def p1(self):
        return [RSymbol()]

    def p2(self):
        return []

class ASymbol(NonTerminalSymbol):
    def __init__(self) -> None:
        super().__init__()
        self.productions = [self.p1, self.p2]

    def p1(self):
        return [aSymbol()]

    def p2(self):
        return [faSymbol()]

class BSymbol(NonTerminalSymbol):
    def __init__(self) -> None:
        super().__init__()
        self.productions = [self.p1, self.p2]

    def p1(self):
        return [bSymbol()]
    
    def p2(self):
        return [fbSymbol()]

class RSymbol(NonTerminalSymbol):
    def __init__(self) -> None:
        super().__init__()
        self.productions = [self.p1, self.p2]

    def p1(self):
        return [rSymbol()]
    
    def p2(self):
        return [frSymbol()]

class CSymbol(NonTerminalSymbol):
    def __init__(self) -> None:
        super().__init__()
        self.productions = [self.p1]

    def p1(self):
        return [cSymbol()]
    
