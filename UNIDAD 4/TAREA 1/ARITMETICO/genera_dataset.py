import random
import pandas as pd

# Operaciones posibles
ops = ['+', '-', '*', '/']


# Generar dataset
data = []
for _ in range(10000):
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    op = random.choice(ops)
    
    if op == '/' and b == 0:  # evitar división por 0
        b = 1
    expr = f"{a}{op}{b}"
    result = eval(expr)
    data.append([a, op, b, result])

df = pd.DataFrame(data, columns=['a', 'op', 'b', 'result'])
df.to_csv("dataset_operaciones.csv", index=False)
print(df.head())
