"""Expression parser using Shunting-yard algorithm. Converts infix to postfix (RPN)."""
import re
from enum import Enum, auto
from typing import Union

class TokenType(Enum):
    NUMBER = auto()
    OPERATOR = auto()
    FUNCTION = auto()
    PAREN_LEFT = auto()
    PAREN_RIGHT = auto()
    COMMA = auto()
    VARIABLE = auto()
    CONSTANT = auto()
    FACTORIAL = auto()

class Token:
    __slots__ = ('type', 'value', 'precedence', 'associativity')
    def __init__(self, token_type: TokenType, value: str, precedence: int = 0, associativity: str = 'left'):
        self.type = token_type
        self.value = value
        self.precedence = precedence
        self.associativity = associativity
    def __repr__(self): return f"Token({self.type}, {self.value})"

PRECEDENCE = {
    '+': 1, '-': 1,
    '×': 2, '*': 2, '÷': 2, '/': 2, '%': 2, 'mod': 2,
    '**': 3, '^': 3,
    '~': 4, '!': 4,
}

FUNCTIONS = {
    'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
    'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
    'ln', 'log', 'log2', 'log10',
    'sqrt', 'cbrt', 'abs', 'exp',
    'ceil', 'floor', 'round',
    'factorial',
    'sec', 'csc', 'cot', 'asec', 'acsc', 'acot',
}

CONSTANTS = {'π': 3.141592653589793, 'pi': 3.141592653589793, 'e': 2.718281828459045, 'phi': 1.618033988749895}

class ExpressionTokenizer:
    """Tokenizes mathematical expressions."""
    
    SYMBOL_MAP = {
        '×': '*', '÷': '/', '−': '-', '^': '**',
        '·': '*', '⁄': '/', 'x': '*',
    }
    
    def tokenize(self, expression: str) -> list[Token]:
        tokens = []
        i = 0
        expr = expression.strip()
        while i < len(expr):
            ch = expr[i]
            if ch.isspace():
                i += 1
                continue
            # Hex numbers (0x...)
            if ch == '0' and i + 1 < len(expr) and expr[i+1] in 'xX':
                num_str = '0x'
                i += 2
                while i < len(expr) and expr[i] in '0123456789abcdefABCDEF':
                    num_str += expr[i]
                    i += 1
                tokens.append(Token(TokenType.NUMBER, str(int(num_str, 16))))
                continue
            # Binary numbers (0b...)
            if ch == '0' and i + 1 < len(expr) and expr[i+1] in 'bB':
                num_str = '0b'
                i += 2
                while i < len(expr) and expr[i] in '01':
                    num_str += expr[i]
                    i += 1
                tokens.append(Token(TokenType.NUMBER, str(int(num_str, 2))))
                continue
            if ch.isdigit() or ch == '.':
                num_str = ''
                while i < len(expr) and (expr[i].isdigit() or expr[i] in '.eE'):
                    if expr[i] in 'eE':
                        num_str += expr[i]
                        i += 1
                        if i < len(expr) and expr[i] in '+-':
                            num_str += expr[i]
                            i += 1
                    else:
                        num_str += expr[i]
                        i += 1
                tokens.append(Token(TokenType.NUMBER, num_str))
                continue
            if ch in '+-':
                if not tokens or tokens[-1].type in (TokenType.OPERATOR, TokenType.PAREN_LEFT, TokenType.COMMA, TokenType.FUNCTION):
                    if ch == '-':
                        tokens.append(Token(TokenType.OPERATOR, 'u-', 5, 'right'))
                    i += 1
                    continue
                tokens.append(Token(TokenType.OPERATOR, ch, 1, 'left'))
                i += 1
                continue
            if ch == '*' and i + 1 < len(expr) and expr[i + 1] == '*':
                tokens.append(Token(TokenType.OPERATOR, '**', 3, 'right'))
                i += 2
                continue
            if ch in '×÷*/%':
                mapped = self.SYMBOL_MAP.get(ch, ch)
                tokens.append(Token(TokenType.OPERATOR, mapped, PRECEDENCE.get(mapped, 2), 'left'))
                i += 1
                continue
            if ch == '^':
                tokens.append(Token(TokenType.OPERATOR, '**', 3, 'right'))
                i += 1
                continue
            if ch == '!':
                tokens.append(Token(TokenType.FACTORIAL, '!', 4, 'left'))
                i += 1
                continue
            if ch == '~':
                tokens.append(Token(TokenType.OPERATOR, '~', 5, 'right'))
                i += 1
                continue
            if expr[i:i+3].lower() == 'mod':
                tokens.append(Token(TokenType.OPERATOR, '%', 2, 'left'))
                i += 3
                continue
            if ch == '(':
                tokens.append(Token(TokenType.PAREN_LEFT, '('))
                i += 1
                continue
            if ch == ')':
                tokens.append(Token(TokenType.PAREN_RIGHT, ')'))
                i += 1
                continue
            if ch == ',':
                tokens.append(Token(TokenType.COMMA, ','))
                i += 1
                continue
            if expr[i:i+2] == 'π':
                tokens.append(Token(TokenType.CONSTANT, 'π'))
                i += 2
                continue
            if expr[i] == 'π':
                tokens.append(Token(TokenType.CONSTANT, 'π'))
                i += 1
                continue
            if ch.isalpha() or ch == '_':
                word = ''
                while i < len(expr) and (expr[i].isalnum() or expr[i] == '_'):
                    word += expr[i]
                    i += 1
                word_lower = word.lower()
                if word_lower in CONSTANTS or word in CONSTANTS:
                    tokens.append(Token(TokenType.CONSTANT, word if word in CONSTANTS else word_lower))
                elif word_lower in FUNCTIONS:
                    tokens.append(Token(TokenType.FUNCTION, word_lower, 6, 'left'))
                else:
                    tokens.append(Token(TokenType.VARIABLE, word_lower))
                continue
            i += 1
        return tokens


class ShuntingYardParser:
    """Infix to postfix (RPN) converter using Shunting-yard algorithm."""
    
    def __init__(self):
        self._tokenizer = ExpressionTokenizer()
    
    def parse(self, expression: str) -> list[Token]:
        """Convert infix expression to postfix (RPN) token list."""
        tokens = self._tokenizer.tokenize(expression)
        output: list[Token] = []
        op_stack: list[Token] = []
        
        for token in tokens:
            if token.type == TokenType.NUMBER:
                output.append(token)
            elif token.type == TokenType.CONSTANT:
                output.append(token)
            elif token.type == TokenType.VARIABLE:
                output.append(token)
            elif token.type == TokenType.FUNCTION:
                op_stack.append(token)
            elif token.type == TokenType.COMMA:
                while op_stack and op_stack[-1].type != TokenType.PAREN_LEFT:
                    output.append(op_stack.pop())
            elif token.type in (TokenType.OPERATOR, TokenType.FACTORIAL):
                while (op_stack and op_stack[-1].type in (TokenType.OPERATOR, TokenType.FACTORIAL) and
                       ((op_stack[-1].precedence > token.precedence) or
                        (op_stack[-1].precedence == token.precedence and token.associativity == 'left'))):
                    output.append(op_stack.pop())
                op_stack.append(token)
            elif token.type == TokenType.PAREN_LEFT:
                op_stack.append(token)
            elif token.type == TokenType.PAREN_RIGHT:
                while op_stack and op_stack[-1].type != TokenType.PAREN_LEFT:
                    output.append(op_stack.pop())
                if op_stack:
                    op_stack.pop()  # Remove left paren
                if op_stack and op_stack[-1].type == TokenType.FUNCTION:
                    output.append(op_stack.pop())
        
        while op_stack:
            if op_stack[-1].type == TokenType.PAREN_LEFT:
                raise ValueError("Unmatched parentheses")
            output.append(op_stack.pop())
        
        return output
    
    def tokenize_only(self, expression: str) -> list[Token]:
        return self._tokenizer.tokenize(expression)
