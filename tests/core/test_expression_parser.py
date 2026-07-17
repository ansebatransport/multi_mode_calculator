import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.expression_parser import ShuntingYardParser, Token, TokenType


class TestShuntingYardParser(unittest.TestCase):
    def setUp(self):
        self.parser = ShuntingYardParser()

    def _types(self, expression):
        return [t.type for t in self.parser.parse(expression)]

    def _values(self, expression):
        return [t.value for t in self.parser.parse(expression)]

    def test_simple_addition(self):
        result = self.parser.parse("2+3")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].type, TokenType.NUMBER)
        self.assertEqual(result[1].type, TokenType.NUMBER)
        self.assertEqual(result[2].type, TokenType.OPERATOR)
        self.assertEqual(result[2].value, "+")

    def test_operator_precedence(self):
        values = self._values("2+3*4")
        self.assertEqual(values, ["2", "3", "4", "*", "+"])

    def test_parentheses(self):
        values = self._values("(2+3)*4")
        self.assertEqual(values, ["2", "3", "+", "4", "*"])

    def test_deeply_nested_parentheses(self):
        values = self._values("((1+2)*(3+4))")
        self.assertEqual(values, ["1", "2", "+", "3", "4", "+", "*", ])

    def test_unary_minus_at_start(self):
        tokens = self.parser.tokenize_only("-5")
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].type, TokenType.OPERATOR)
        self.assertEqual(tokens[0].value, "u-")
        self.assertEqual(tokens[1].type, TokenType.NUMBER)
        self.assertEqual(tokens[1].value, "5")

    def test_unary_minus_after_operator(self):
        tokens = self.parser.parse("2*-3")
        values = [t.value for t in tokens]
        self.assertIn("u-", values)

    def test_function_token(self):
        tokens = self.parser.tokenize_only("sin(30)")
        types = [t.type for t in tokens]
        self.assertIn(TokenType.FUNCTION, types)
        func_token = [t for t in tokens if t.type == TokenType.FUNCTION][0]
        self.assertEqual(func_token.value, "sin")

    def test_nested_function_tokens(self):
        tokens = self.parser.tokenize_only("sin(cos(0))")
        funcs = [t for t in tokens if t.type == TokenType.FUNCTION]
        func_names = [f.value for f in funcs]
        self.assertIn("sin", func_names)
        self.assertIn("cos", func_names)

    def test_constant_pi(self):
        tokens = self.parser.tokenize_only("π+1")
        consts = [t for t in tokens if t.type == TokenType.CONSTANT]
        self.assertEqual(len(consts), 1)
        self.assertEqual(consts[0].value, "π")

    def test_constant_euler(self):
        tokens = self.parser.tokenize_only("e+1")
        consts = [t for t in tokens if t.type == TokenType.CONSTANT]
        self.assertEqual(len(consts), 1)
        self.assertEqual(consts[0].value, "e")

    def test_variable(self):
        tokens = self.parser.tokenize_only("x+1")
        vars_ = [t for t in tokens if t.type == TokenType.VARIABLE]
        self.assertEqual(len(vars_), 1)
        self.assertEqual(vars_[0].value, "x")

    def test_mod_keyword(self):
        values = self._values("10 mod 3")
        self.assertIn("%", values)

    def test_caret_as_power(self):
        values = self._values("2^3")
        self.assertIn("**", values)

    def test_unmatched_parens(self):
        with self.assertRaises(ValueError):
            self.parser.parse("(2+3")

    def test_empty_expression(self):
        result = self.parser.parse("")
        self.assertEqual(result, [])

    def test_whitespace_handling(self):
        values = self._values("  2   +   3  ")
        self.assertEqual(values, ["2", "3", "+"])

    def test_hex_number(self):
        tokens = self.parser.tokenize_only("0xFF")
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, "255")

    def test_binary_number(self):
        tokens = self.parser.tokenize_only("0b1010")
        self.assertEqual(tokens[0].type, TokenType.NUMBER)
        self.assertEqual(tokens[0].value, "10")

    def test_precedence_chain(self):
        values = self._values("1+2*3^4")
        self.assertEqual(values[-1], "+")
        self.assertEqual(values[-2], "*")
        self.assertEqual(values[-3], "**")

    def test_right_associativity_power(self):
        values = self._values("2**3**2")
        self.assertEqual(values, ["2", "3", "2", "**", "**"])

    def test_function_with_multiple_args_tokenized(self):
        tokens = self.parser.tokenize_only("max(1,2)")
        commas = [t for t in tokens if t.type == TokenType.COMMA]
        self.assertEqual(len(commas), 1)


if __name__ == "__main__":
    unittest.main()
