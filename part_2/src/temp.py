from tkinter import Y


x = [["one", "two"] , ["three", "four"]]
y = x
z = list(x)
tx = tuple(tuple(i) for i in x)
lx = list(list(i) for i in tx)

print("x =", x)
print("y =", y)
print("z =", z)
print("x is y? ", x is y)
print("x is z? ", x is z)

print("x        =", x)
print("tuple(x) =", tx)
print("list(tx) =", lx)

print("tx=", tx[1][0][0])


