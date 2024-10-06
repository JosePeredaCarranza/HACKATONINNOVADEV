from flask import Flask, flash
from .entities.User import User
import os
import pandas as pd


class ModelSpreadsheets():

    @classmethod
    def countRows(self,data):
        data_filas = data.shape[0]
        return data_filas
    
    @classmethod
    def checkFormat(cls, data):
        data_columnas = data.columns.tolist()
        if len(data_columnas) >= 6 and data_columnas[0:6] == ['CODIGO', 'DNI','CORREO', 'NOMBRES', 'APELLIDOS', 'ROL']:
            return True
        else:
            return False
