import pandas as pd

def main():
    # Intentar cargar el archivo de gastos
    try:
        df = pd.read_csv("gastos.csv")
    except FileNotFoundError:
        print("No se encontró el archivo 'gastos.csv'.")
        print("Asegúrate de montarlo como volumen o copiarlo dentro del contenedor.")
        return

    # Mostrar primeros registros
    print("\nPrimeros registros del archivo:")
    print(df.head())

    # Gasto total
    total = df["amount"].sum()
    print(f"\nGasto total: {total:.2f}")

    # Gasto por categoría
    print("\nGasto por categoría:")
    print(df.groupby("category")["amount"].sum())

    # Gasto promedio
    promedio = df["amount"].mean()
    print(f"\nGasto promedio: {promedio:.2f}")


if __name__ == "__main__":
    main()
