# Gauss-Jordan Solver App

Aplicación gráfica para resolver sistemas de ecuaciones lineales 4x4 utilizando el método de Gauss-Jordan con pivoteo parcial.

## Características

- Interfaz intuitiva tipo hoja de cálculo para entrada de coeficientes
- Validación de datos de entrada
- Soporte para sistemas con solución única
- Resultados con 4 decimales de precisión
- Implementación con principios SOLID y POO
- Pivoteo parcial para estabilidad numérica
- Navegación mejorada mediante teclado (Enter, Tab)
- Atajos de teclado (Ctrl+R para resolver, Ctrl+C para limpiar)
- Botón de limpieza para reiniciar todos los campos

## Requisitos

- Python 3.10 (versión compatible con tkinter)
- Paquete `python3-tk` (en sistemas Linux)
- Numpy 1.21+

## Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/tu-usuario/gauss_jordan_app.git
cd gauss_jordan_app
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install numpy
```

## Uso

1. Ejecutar la aplicación:

```bash
python3.10  main.py
```

2. Ingresar los coeficientes de las ecuaciones en la matriz 4x4
3. Hacer clic en "Resolver" o presionar Ctrl+R
4. Los resultados se mostrarán en el panel derecho

## Ejemplos

### Sistema de ejemplo:

```
2x + 1y - 1z + 3w = 1
3x - 2y + 2z + 1w = 2
1x + 3y - 3z - 2w = 0
4x - 1y + 5z + 0w = 3
```

### Solución esperada:

```
x = 1.0000
y = -1.0000
z = 2.0000
w = 0.0000
```

## Manejo de errores

La aplicación detecta y maneja los siguientes errores:

- Valores no numéricos
- Sistemas sin solución única
- Matrices singulares

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Sube tu rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Créditos

Desarrollado como parte del curso de Métodos Numéricos.
