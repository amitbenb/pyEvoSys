import math


def add(a, b): return a + b
def sub(a, b): return a - b
def uminus(a): return - a
def mult(a, b): return a * b
def double_f(a): return a
def safe_dev(a, b): return a / b if b != 0 else b
def one(a, b): return a / b if b != 0 else b
def left(a, _): return a
def right(_, b): return b
def if0(a, b, c): return b if a == 0 else c
def ifle(a, b, c, d): return c if a <= b else d
def sin(a): return math.sin(a)
def cos(a): return math.cos(a)
def tan(a): return math.tan(a)
def cot(a): return 1/math.tan(a)

