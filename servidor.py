from flask import Flask, request, jsonify, render_template_string, session
from werkzeug.security import generate_password_hash, check_password_hash
import db

# Configuración del servidor
app = Flask(__name__)
app.secret_key = "clave_secreta_simple"

# Inicializa SQLite
db.init_db()


@app.route("/")
def inicio():
    return jsonify({"mensaje": "Servidor funcionando"})


@app.route("/registro", methods=["POST"])
def registro():
    try:
        data = request.get_json(silent=True) or {}

        usuario = data.get("usuario", "").strip()
        contrasena = data.get("contraseña", "").strip()

        # Valida datos obligatorios
        if not usuario or not contrasena:
            return jsonify({"error": "Faltan datos"}), 400

        # Evita registrar dos veces el mismo usuario
        if db.usuario_existe(usuario):
            return jsonify({"error": "El usuario ya existe"}), 409

        # Hashea la contraseña antes de guardarla
        hash_contrasena = generate_password_hash(contrasena)
        db.crear_usuario(usuario, hash_contrasena)

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(silent=True) or {}

        usuario = data.get("usuario", "").strip()
        contrasena = data.get("contraseña", "").strip()

        # Valida datos obligatorios
        if not usuario or not contrasena:
            return jsonify({"error": "Faltan datos"}), 400

        fila = db.obtener_usuario(usuario)

        # Verifica si el usuario existe
        if fila is None:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        # Compara la contraseña con el hash guardado
        if not check_password_hash(fila["contrasena"], contrasena):
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        # Guarda el usuario en sesión
        session["usuario"] = usuario

        return jsonify({"mensaje": f"Bienvenido, {usuario}!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/tareas", methods=["GET"])
def tareas():
    usuario = session.get("usuario")

    html = """
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Gestor de Tareas</title>
    </head>
    <body>
        <h1>Sistema de Gestión de Tareas</h1>
        {% if usuario %}
            <p>Bienvenido, <strong>{{ usuario }}</strong>.</p>
        {% else %}
            <p>Bienvenido. Iniciá sesión para continuar.</p>
        {% endif %}
    </body>
    </html>
    """

    return render_template_string(html, usuario=usuario)


if __name__ == "__main__":
    print("Servidor corriendo en http://localhost:5000")
    app.run(debug=True, port=5000)