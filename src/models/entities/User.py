from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from config import Config


class User(UserMixin):

    def __init__(self, id_usuario, codigo, dni, correo, contra, nombre = "", apellido = "", rol = "") -> None:
        self.id_usuario = id_usuario
        self.codigo = codigo
        self.dni = dni
        self.correo = correo
        self.contra = contra
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol
    
    def get_id(self):
        return str(self.id_usuario) 
    
    @classmethod
    def check_password(self, hashed_password, contra):
        return check_password_hash(hashed_password,contra)
    
    @classmethod
    def generate_passHash(self, contra):
        return generate_password_hash(contra)
    
    def generate_token(self, correo):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        return serializer.dumps(correo, salt='recovery-salt')
    
    @classmethod
    def verify_token(self, token, expiration=600):
        serializer = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:
            email = serializer.loads(token, salt='recovery-salt', max_age=expiration)
        except:
            return False
        return email