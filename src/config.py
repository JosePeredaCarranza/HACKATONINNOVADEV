from flask import Flask

class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'miguel123456'
    MYSQL_DB = 'gestion_espacios'

config = {
    'development': DevelopmentConfig
}