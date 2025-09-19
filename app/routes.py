from flask import Blueprint, render_template, url_for, redirect, request, flash, abort
# Importar los modelos y la instancia de la base de datos
from .models import db, Programa, Usuario

# Creación del Blueprint
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route("/")
def home_redirect():
    # Redirige de la raíz a la página de inicio
    return redirect(url_for('main.index'))

@bp.route("/index")
def index():
    return render_template('index.html')

@bp.route("/mision")
def mision():
    return render_template('mision.html')

@bp.route("/vision")
def vision():
    return render_template('vision.html')

@bp.route("/programas", methods=['GET', 'POST'])
def programas():
    if request.method == 'POST':
        # Asumimos que el formulario envía 'nombre_programa'
        nombre_programa = request.form.get('nombre_programa')
        
        if nombre_programa:
            # Verificar si el programa ya existe
            if not Programa.query.filter_by(nombre=nombre_programa).first():
                nuevo_programa = Programa(nombre=nombre_programa)
                db.session.add(nuevo_programa)
                db.session.commit()
                flash(f'Programa "{nombre_programa}" añadido exitosamente.', 'success')
            else:
                flash(f'El programa "{nombre_programa}" ya existe.', 'warning')
        else:
            flash('El nombre del programa no puede estar vacío.', 'danger')
            
        return redirect(url_for('main.programas'))
    
    # Muestra la lista de programas en el método GET
    lista_programas = Programa.query.all()
    return render_template('programas.html', programas=lista_programas)

# --- Rutas para CRUD de Programas ---

@bp.route("/programas/edit/<int:id>", methods=['GET', 'POST'])
def edit_programa(id):
    programa = Programa.query.get_or_404(id) # Obtener programa o abortar con 404

    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre_programa')
        if nuevo_nombre:
            # Verificar si el nuevo nombre ya existe en otro programa
            existing_programa = Programa.query.filter(
                Programa.nombre == nuevo_nombre,
                Programa.id != id
            ).first()
            if existing_programa:
                flash(f'El programa "{nuevo_nombre}" ya existe.', 'warning')
            else:
                programa.nombre = nuevo_nombre
                db.session.commit()
                flash(f'Programa "{programa.nombre}" actualizado exitosamente.', 'success')
                return redirect(url_for('main.programas'))
        else:
            flash('El nombre del programa no puede estar vacío.', 'danger')
            
    return render_template('edit_programa.html', programa=programa)

@bp.route("/programas/delete/<int:id>", methods=['POST'])
def delete_programa(id):
    programa = Programa.query.get_or_404(id) # Obtener programa o abortar con 404
    db.session.delete(programa)
    db.session.commit()
    flash(f'Programa "{programa.nombre}" eliminado exitosamente.', 'success')
    return redirect(url_for('main.programas'))


# --- Rutas de Autenticación (Ejemplo de implementación segura) ---

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([nombre, email, password]):
            flash('Todos los campos son requeridos.', 'danger')
            return redirect(url_for('main.register'))

        # Verificar si el email ya está registrado
        if Usuario.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado.', 'warning')
            return redirect(url_for('main.register'))

        # Crear nuevo usuario y hashear la contraseña
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.set_password(password) # ¡Uso del método seguro!
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html') # Necesitaremos crear esta plantilla

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([email, password]):
            flash('Todos los campos son requeridos.', 'danger')
            return redirect(url_for('main.login'))

        usuario = Usuario.query.filter_by(email=email).first()
        
        # Verificar que el usuario existe y la contraseña es correcta
        if not usuario or not usuario.check_password(password): # ¡Uso del método seguro!
            flash('Correo o contraseña incorrectos.', 'danger')
            return redirect(url_for('main.login'))
        
        # Aquí iría la lógica para iniciar sesión (ej. con Flask-Login)
        # from flask_login import login_user
        # login_user(usuario)
        
        flash('Inicio de sesión exitoso.', 'success')
        return redirect(url_for('main.index'))

    return render_template('login.html') # Necesitaremos crear esta plantilla
