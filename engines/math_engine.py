"""
Evaluates arithmetic expressions by walking a parsed AST directly — no
eval() involved, so there's no interpreter to escape from. Only whitelisted
operators, functions and constants are reachable from _eval.
"""

import ast
import math
import operator
from typing import Callable, Dict, Type

_Number = float

_BIN_OPS: Dict[Type[ast.operator], Callable[[_Number, _Number], _Number]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}
_UNARY_OPS: Dict[Type[ast.unaryop], Callable[[_Number], _Number]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class MathEngine:
    _BIN_OPS = _BIN_OPS
    _UNARY_OPS = _UNARY_OPS
    _FUNCTIONS: Dict[str, Callable[..., float]] = {
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log10,
        "ln": math.log,
    }
    _CONSTANTS: Dict[str, float] = {
        "pi": math.pi,
        "e": math.e,
    }

    @classmethod
    def solve(cls, expression: str) -> str:
        expr = expression.strip().replace("^", "**")
        if not expr:
            return "❌ Syntax Error"
        try:
            tree = ast.parse(expr, mode="eval")
            result = cls._eval(tree.body)
        except ZeroDivisionError:
            return "♾️ Infinity"
        except SyntaxError:
            return "❌ Syntax Error"
        except (ValueError, TypeError):
            return "❌ Error: Disallowed expression"
        except Exception:
            return "❌ Syntax Error"

        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))
            return f"{result:.4f}"
        return str(result)

    @classmethod
    def _eval(cls, node: ast.AST) -> float:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(
                node.value, bool
            ):
                return node.value
            raise ValueError("Invalid constant")

        if isinstance(node, ast.BinOp):
            op_func = cls._BIN_OPS.get(type(node.op))
            if op_func is None:
                raise ValueError("Unsupported operator")
            return op_func(cls._eval(node.left), cls._eval(node.right))

        if isinstance(node, ast.UnaryOp):
            unary_op_func = cls._UNARY_OPS.get(type(node.op))
            if unary_op_func is None:
                raise ValueError("Unsupported operator")
            return unary_op_func(cls._eval(node.operand))

        if isinstance(node, ast.Call):
            if (
                not isinstance(node.func, ast.Name)
                or node.func.id not in cls._FUNCTIONS
                or node.keywords
            ):
                raise ValueError("Unsupported function call")
            args = [cls._eval(arg) for arg in node.args]
            return cls._FUNCTIONS[node.func.id](*args)

        if isinstance(node, ast.Name):
            if node.id in cls._CONSTANTS:
                return cls._CONSTANTS[node.id]
            raise ValueError("Unknown identifier")

        raise ValueError("Unsupported expression")
