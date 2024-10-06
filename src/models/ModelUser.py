from flask import flash
from .entities.User import User
import random

minus="abcdefghijklmnopqrstuvwxyz"
mayus= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
number="1234567890"
longitud=9
random_pass = minus + mayus + number


class ModelUser():

    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_usuario, codigo, dni, nombre, apellido, correo, contra, rol FROM gestion_espacios.usuarios WHERE correo = %s ", (user.correo,))
            row=cursor.fetchone()
            if row != None:
                user=User(row[0], row[1], row[2], row[5], User.check_password(row[6], user.contra))
                return user
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_usuario, codigo, dni, nombre, apellido, correo, rol FROM gestion_espacios.usuarios WHERE id_usuario = %s", (id,))
            row=cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2], row[5], None, row[3], row[4])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_mail(self,db,mail):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_usuario, codigo, dni, nombre, apellido, correo, rol FROM gestion_espacios.usuarios WHERE correo = %s", (mail,))
            row=cursor.fetchone()
            if row != None:
                return User(row[0], row[1], row[2], row[5], None, row[3], row[4])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def register(self,db,user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_usuario, codigo, dni, nombre, apellido, correo, contra, rol FROM gestion_espacios.usuarios WHERE correo = %s ", (user.correo,))
            row=cursor.fetchone()
            if row == None:
                try:
                    new_random_pass = random.sample(random_pass,longitud)
                    new_random_pass = "".join(new_random_pass)
                    newpass = User.generate_passHash(new_random_pass)
                    cursor.execute("""INSERT INTO gestion_espacios.usuarios (codigo, dni, nombre, apellido, correo, contra, rol)
                                   VALUES (%s,%s,%s,%s,%s,%s,%s) """, (user.codigo,user.dni,user.nombre,user.apellido,user.correo,newpass,user.rol, ))
                    db.connection.commit()
                    user.contra=new_random_pass
                except Exception as ex_1:
                    raise Exception(f"Ocurrió un error en el guardado: {str(ex_1)}") from ex_1
                return user
            else:
                flash("El correo ya está registrado.")
                return None
            
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def change_password(self,db,user,password):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_usuario, codigo, dni, nombre, apellido, correo, contra, rol FROM gestion_espacios.usuarios WHERE correo = %s ", (user.correo,))
            row=cursor.fetchone()
            if row != None:
                try:
                    newpass = User.generate_passHash(password)
                    cursor.execute("UPDATE gestion_espacios.usuarios SET contra = %s WHERE correo = %s ", (newpass, user.correo))
                    db.connection.commit()
                except Exception as ex_1:
                    raise Exception("Ocurrió un error en el guardado de la nueva contraseña") from ex_1
                return user
            else:
                flash("El correo no existe.")
                return None
            
        except Exception as ex:
            raise Exception(ex)
