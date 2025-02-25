import pandas as pd

data = {
    'id': [1, 2, 3, 4, 5],
    'nome': ['Alice', 'Bob', 'Carlos', 'Daniel', 'Eva'],
    'idade': [25, 30, 35, 40, 45],
    'salario': [5000, 7000, 8000, 10000, 12000]
}

df = pd.DataFrame(data)
media = df[df['idade'] > 30]['salario'].mean()
print("Média salarial para idade > 30:", media)
#