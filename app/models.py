from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Se crea una instancia de SQLAlchemy sin vincularla a una app todavía.
# La vinculación se hará en la factory de la aplicación.
db = SQLAlchemy()

class Programa(db.Model):
    __tablename__ = 'programas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'<Programa {self.nombre}>'

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False) # Se almacenará el hash
    fecha_registro = db.Column(db.TIMESTAMP(timezone=True), server_default=db.func.now())

    def set_password(self, password):
        """Crea un hash de la contraseña y la almacena."""
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con el hash almacenado."""
        return check_password_hash(self.contrasena, password)

    def __repr__(self):
        return f'<Usuario {self.email}>'