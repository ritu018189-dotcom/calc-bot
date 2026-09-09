from engines.math_engine import MathEngine


def test_basic_arithmetic():
    assert MathEngine.solve("10+20") == "30"
    assert MathEngine.solve("2*3") == "6"
    assert MathEngine.solve("7-2") == "5"


def test_division():
    assert MathEngine.solve("10/4") == "2.5000"


def test_division_by_zero():
    assert MathEngine.solve("5/0") == "♾️ Infinity"


def test_power():
    assert MathEngine.solve("2^10") == "1024"


def test_sqrt():
    assert MathEngine.solve("sqrt(144)") == "12"


def test_constants():
    assert MathEngine.solve("pi") == "3.1416"


def test_rejects_disallowed_calls():
    assert MathEngine.solve("__import__('os')") == "❌ Error: Disallowed expression"
    assert MathEngine.solve("open('/etc/passwd')") == "❌ Error: Disallowed expression"


def test_rejects_unknown_identifiers():
    assert MathEngine.solve("os") == "❌ Error: Disallowed expression"


def test_rejects_bad_syntax():
    assert MathEngine.solve("10+") == "❌ Syntax Error"
    assert MathEngine.solve("") == "❌ Syntax Error"
