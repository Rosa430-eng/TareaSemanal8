import os
import subprocess

SALIR = '0'
VOLVER_MENU = '9'


def leer_archivo(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None


def ejecutar_script(ruta):
    try:
        if os.name == 'nt':
            subprocess.Popen(['cmd', '/k', 'python', ruta])
        else:
            subprocess.Popen(['python3', ruta])
    except Exception as e:
        print(f"Error al ejecutar el script: {e}")


def imprimir_menu(titulo, opciones):
    print(f"\n===== {titulo} =====")
    for k, v in opciones.items():
        print(f"{k} - {v}")
    print("0 - Salir")


def mostrar_dashboard():
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2'
    }

    while True:
        imprimir_menu("DASHBOARD", unidades)
        opcion = input("Seleccione una opción: ")

        if opcion == SALIR:
            print("Saliendo del sistema...")
            break
        elif opcion in unidades:
            ruta = os.path.join(ruta_base, unidades[opcion])
            navegar_carpetas(ruta)
        else:
            print("Opción inválida.")


def navegar_carpetas(ruta_unidad):
    if not os.path.exists(ruta_unidad):
        print("La unidad no existe.")
        return

    carpetas = [c.name for c in os.scandir(ruta_unidad) if c.is_dir()]

    if not carpetas:
        print("No hay subcarpetas.")
        return

    while True:
        print("\n--- SUBCARPETAS ---")
        for i, carpeta in enumerate(carpetas, 1):
            print(f"{i} - {carpeta}")
        print("0 - Volver")

        opcion = input("Seleccione una carpeta: ")

        if opcion == SALIR:
            return

        try:
            index = int(opcion) - 1
            ruta_sub = os.path.join(ruta_unidad, carpetas[index])
            navegar_scripts(ruta_sub)
        except (ValueError, IndexError):
            print("Selección inválida.")


def navegar_scripts(ruta_sub):
    scripts = [s.name for s in os.scandir(ruta_sub) if s.is_file() and s.name.endswith('.py')]

    if not scripts:
        print("No hay scripts disponibles.")
        return

    while True:
        print("\n--- SCRIPTS ---")
        for i, script in enumerate(scripts, 1):
            print(f"{i} - {script}")
        print("0 - Volver")
        print("9 - Menú principal")

        opcion = input("Seleccione un script: ")

        if opcion == SALIR:
            return
        if opcion == VOLVER_MENU:
            raise SystemExit

        try:
            index = int(opcion) - 1
            ruta_script = os.path.join(ruta_sub, scripts[index])

            codigo = leer_archivo(ruta_script)
            if codigo:
                print("\n--- CÓDIGO ---\n")
                print(codigo)
                ejecutar = input("¿Ejecutar? (1=Sí / 0=No): ")
                if ejecutar == '1':
                    ejecutar_script(ruta_script)

        except (ValueError, IndexError):
            print("Selección inválida.")


if __name__ == "__main__":
    try:
        mostrar_dashboard()
    except SystemExit:
        mostrar_dashboard()


