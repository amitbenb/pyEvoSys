import math
import random


# def identity(x): return x
# def random_function_generator(a,b):
#     return lambda: random.random()*(b-a) + a


def add(a, b): return a + b
# add.children = (('l','r'))
def sub(a, b): return a - b
# sub.children = (('l','r'))
def uminus(a): return - a
# uminus.children = (('l'))
def mult(a, b): return a * b
def max_f(a,b): return max(a,b)
def min_f(a,b): return min(a,b)
def double_f(a): return 2 * a
# double_f.children = (('l'))
def safe_div(a, b): return a / b if b != 0 else b
# def one(a, b): return a / b if b != 0 else b
def left(a, _): return a
def right(_, b): return b
def if0(a, b, c): return b if a == 0 else c
# if0.children = (('l','rl','rr'))
# if0.children = (('ll','rl','r'))
def ifle(a, b, c, d): return c if a <= b else d
# ifle.children = (('ll','lr','rl','rr'))
def sin(a): return math.sin(a)
def cos(a): return math.cos(a)
def tan(a): return math.tan(a)
def cot(a): return 1/math.tan(a)


def lower(a, b): return a < b
def greater(a, b): return a > b
def le(a, b): return a <= b
def ge(a, b): return a >= b
def andf(a, b): return a and b
def orf(a, b): return a or b
def notf(a): return not a

