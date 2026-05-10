import requests

BASE_URL = "http://127.0.0.1:5000"
sesion = requests.Session()


def registrar():
    print("\n--- Registro de usuario ---")
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    r = sesion.post(
        f"{BASE_URL}/registro",
        json={"usuario": usuario, "contraseña": contrasena}
    )

    print(f"Código: {r.status_code}")
    print(f"Respuesta: {r.json()}")


def login():
    print("\n--- Inicio de sesión ---")
    usuario = input("Usuario: ").strip()
    contrasena = input("Contraseña: ").strip()

    r = sesion.post(
        f"{BASE_URL}/login",
        json={"usuario": usuario, "contraseña": contrasena}
    )

    print(f"Código: {r.status_code}")
    print(f"Respuesta: {r.json()}")


def ver_tareas():
    print("\n--- GET /tareas ---")
    r = sesion.get(f"{BASE_URL}/tareas")
    print(f"Código: {r.status_code}")
    print(r.text)


def menu():
    while True:
        print("\n=== MENÚ ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver /tareas")
        print("4. Salir")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            login()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            print("Chau!")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()