from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_segura'  # Necesaria para manejar las sesiones de manera segura

# Simulación de una base de datos de usuarios
usuario = {}

# Ruta para la página de inicio donde se encuentra el formulario de inicio de sesión register
@app.route('/')
def index():
    return render_template('entrar.html')

# Ruta para manejar el inicio de sesión users
@app.route('/entrar', methods=['POST'])
def entrar():
    username = request.form['username']
    password = request.form['password']
    
    # Verifica si el usuario existe en la "base de datos"
    if username in usuario and check_password_hash(usuario[username], password):
        session['username'] = username  # Guarda el usuario en la sesión
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('bienvenido'))
    else:
        flash('Nombre de usuario o contraseña incorrectos', 'error')
        return redirect(url_for('index'))

# Ruta para manejar el registro de nuevos usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Verifica que el usuario no esté registrado ya
        if username in usuario:
            flash('El usuario ya está registrado', 'error')
            return redirect(url_for('registro'))
        
        # Almacena el nuevo usuario con la contraseña encriptada
        usuario[username] = generate_password_hash(password)
        flash('Usuario registrado exitosamente', 'success')
        return redirect(url_for('index'))
    
    return render_template('registro.html')

# Ruta para mostrar la página de bienvenida una vez autenticado
@app.route('/bienvenido')
def bienvenido():
    if 'username' in session:
        username = session['username']
        return render_template('bienvenido.html', username=username)
    else:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('index'))

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)  # Elimina el usuario de la sesión
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('index'))

# Ruta para ver la lista de usuarios registrados (solo si está autenticado) login
@app.route('/usuario')
def users_list():
    if 'username' in session:
        return render_template('usuario.html', usuario=usuario)
    else:
        flash('Por favor, inicia sesión primero', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
