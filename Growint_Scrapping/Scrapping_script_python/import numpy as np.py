import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Datos de ejemplo
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)  # Feature (variable independiente)
y = np.array([2, 3, 4, 5, 6])                # Variable dependiente

# Inicializar el modelo de regresión lineal
modelo = LinearRegression()

# Entrenar el modelo
modelo.fit(X, y)

# Coeficiente de la pendiente
print("Pendiente:", modelo.coef_[0])

# Término independiente
print("Intercepto:", modelo.intercept_)

# Hacer predicciones
predicciones = modelo.predict(X)

# Visualizar los datos y la línea de regresión
plt.scatter(X, y, color='blue')
plt.plot(X, predicciones, color='red')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Regresión Lineal Simple')
plt.show()
