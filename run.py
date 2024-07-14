from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import server, database, username, password, driver
import pyodbc
import secrets
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Clave secreta para la sesión

# Configuración de conexión a la base de datos
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']

        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Usuarios WHERE Usuario = ? AND Clave = ?", (user, pwd))
            account = cursor.fetchone()

            if account:
                session['UsuarioId'] = account.Id  # Almacenamos el UsuarioId en la sesión
                if account.Creditos > 0:
                    return redirect(url_for('menu'))
                else:
                    return "Usted no tiene créditos suficientes."
            else:
                return "Usuario o contraseña inválidos"

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email']
        pwd = request.form['password']
        tipo_suscripcion = 'FREE'
        creditos = 10 if tipo_suscripcion == 'FREE' else 0  # Asignar 0 créditos si no es FREE

        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Usuarios (Usuario, Correo, Clave, TipoSuscripcion, Creditos) 
                VALUES (?, ?, ?, ?, ?)""",
                (user, email, pwd, tipo_suscripcion, creditos))
            conn.commit()
        return "Registro exitoso"

    return render_template('register.html')

@app.route('/suscripciones')
def suscripciones():
    return render_template('suscripciones.html')

@app.route('/suscribir', methods=['POST'])
def suscribir():
    usuario_id = session.get('UsuarioId')
    if not usuario_id:
        return redirect(url_for('login'))  # Redirigir al login si no hay sesión activa

    tipo_suscripcion = request.form.get('tipo_suscripcion')

    # Obtener la cantidad de créditos y el precio de la suscripción seleccionada
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Cantidad, Precio FROM Suscripciones WHERE Tipo = ?", (tipo_suscripcion,))
        suscripcion_info = cursor.fetchone()

        if suscripcion_info:
            cantidad = suscripcion_info.Cantidad
            precio = suscripcion_info.Precio

            # Actualizar tipo de suscripción y sumar créditos según el plan seleccionado
            cursor.execute("""
                UPDATE Usuarios 
                SET TipoSuscripcion = ?, Creditos = Creditos + ?
                WHERE Id = ?""",
                (tipo_suscripcion, cantidad, usuario_id))
            conn.commit()

            flash(f"Te has suscrito exitosamente al plan {tipo_suscripcion}.", 'success')
        else:
            flash("No se encontró información para la suscripción seleccionada.", 'error')

    return redirect(url_for('menu'))

@app.route('/menu')
def menu():
    usuario_id = session.get('UsuarioId')
    if not usuario_id:
        return redirect(url_for('login'))  # Redirigir al login si no hay sesión activa

    return render_template('menu.html')

@app.route('/acortar-url', methods=['POST'])
def acortar_url():
    usuario_id = session.get('UsuarioId')
    if not usuario_id:
        return redirect(url_for('login'))  # Redirigir al login si no hay sesión activa

    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Creditos FROM Usuarios WHERE Id = ?", (usuario_id,))
        user_info = cursor.fetchone()

        if user_info.Creditos <= 0:
            flash("No tienes suficientes créditos para acortar una URL.", 'error')
            return redirect(url_for('menu'))

        url_original = request.form['url']
        url_acortada = secrets.token_urlsafe(6)  # Generar un token único como URL acortada

        cursor.execute("""
            INSERT INTO URLs (UsuarioId, URLOriginal, URLAcortada) 
            VALUES (?, ?, ?)""",
            (usuario_id, url_original, url_acortada))
        conn.commit()

        # Reducir un crédito después de acortar la URL
        cursor.execute("UPDATE Usuarios SET Creditos = Creditos - 1 WHERE Id = ?", (usuario_id,))
        conn.commit()

    flash(f"URL acortada exitosamente. Nuevo URL: {url_acortada}", 'success')
    return render_template('menu.html', nueva_url=url_acortada)

@app.route('/perfil')
def perfil():
    usuario_id = session.get('UsuarioId')
    if not usuario_id:
        return redirect(url_for('login'))  # Redirigir al login si no hay sesión activa

    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()

        # Obtener datos personales del usuario
        cursor.execute("SELECT Usuario, Correo, TipoSuscripcion FROM Usuarios WHERE Id = ?", (usuario_id,))
        usuario_info = cursor.fetchone()

        # Obtener URLs acortados por el usuario
        cursor.execute("SELECT URLAcortada, URLOriginal, FechaCreacion FROM URLs WHERE UsuarioId = ?", (usuario_id,))
        urls_acortados = cursor.fetchall()

    return render_template('perfil.html', usuario=usuario_info, urls_acortados=urls_acortados)

@app.route('/logout')
def logout():
    session.pop('UsuarioId', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)