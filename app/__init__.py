import os
from flask import Flask

# Importar la instancia de la base de datos desde models.py
from .models import db

def create_app():
    """
    Factory para crear y configurar la aplicación Flask.
    """
    app = Flask(__name__, instance_relative_config=True)

    # --- Configuración de la Aplicación ---
    # Cargar la SECRET_KEY y DATABASE_URL desde variables de entorno
    secret_key = os.environ.get('SECRET_KEY')
    database_url = os.environ.get('DATABASE_URL')

    # Es CRÍTICO tener una SECRET_KEY segura en producción
    if not secret_key and app.config['ENV'] == 'production':
        raise ValueError("No se ha configurado la SECRET_KEY. Debe establecerse en un entorno de producción.")

    app.config.from_mapping(
        # Usar la variable de entorno o una clave por defecto SOLO para desarrollo
        SECRET_KEY=secret_key or 'a-super-secret-key-for-dev-only',
        SQLALCHEMY_DATABASE_URI=database_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    # Inicializar la base de datos con la aplicación
    db.init_app(app)

    # --- Registro de Blueprints ---
    # El código asume que tienes un Blueprint llamado 'bp' en 'app/routes.py'
    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
