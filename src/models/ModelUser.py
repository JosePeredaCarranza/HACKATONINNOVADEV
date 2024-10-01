from .entities.User import User


class ModelUser():

    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_usuario, nombre, apellido, correo, contra, rol FROM gestion_espacios.usuarios WHERE correo = %s ", (user.correo,))
            row=cursor.fetchone()
            if row != None:
                user=User(row[0], row[3], User.check_password(row[4], user.contra))
                return user
            else:
                return None

        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            cursor.execute("SELECT id_usuario, nombre, apellido, correo, rol FROM gestion_espacios.usuarios WHERE id_usuario = %s", (id,))
            row=cursor.fetchone()
            if row != None:
                return User(row[0], row[3], None, row[1])
            else:
                return None

        except Exception as ex:
            raise Exception(ex)

