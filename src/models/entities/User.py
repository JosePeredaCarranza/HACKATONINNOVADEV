from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id_usuario, correo, contra, nombre = "", apellido = "", rol = "") -> None:
        self.id_usuario = id_usuario
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

#print(generate_password_hash("miguel123"))