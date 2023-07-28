from uclid5_api import *
m = Module("main")

n = m.declare_var("n", integer())
a = m.declare_var("a", integer())
b = m.declare_var("b", integer())
temp = m.declare_var("temp", integer())

m.init.assign(n, 10)
m.init.assign(a, 0)
m.init.assign(b, 1)

with m.next.branch(n > 0) as (then_, else_):
    then_.assign(temp, a + b)
    then_.assign(a, b)
    then_.assign(b, temp)
    then_.assign(n, n - 1)
    then_.goto(then_)
    else_.goto(else_)

print(m)