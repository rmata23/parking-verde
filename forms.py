from wtforms import Form
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators
from wtforms import SelectField

from models import User, Estacionamientos
from main import sEstac

def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacio!.')

class LoginForm(Form):
    username = StringField('Usuario',
                [
                    validators.DataRequired(message = 'El username es requerido!.'),
                    validators.length(min=4, max=25, message='Ingrese un username valido!.')
                ])
    password = PasswordField('Contraseña', [validators.DataRequired(message='El password es requerido!.')])

class UsuariosForm(Form):
    username = StringField('Usuario',
                [
                    validators.DataRequired(message = 'El username es requerido!.'),
                    validators.length(min=4, max=25, message='Ingrese un username valido!.')
                ])
    password = PasswordField('Contraseña', [validators.DataRequired(message='El password es requerido!.')])

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El username ya se encuentra registrado!')

class EntradaForm(Form):
    
    estacionamiento = SelectField('Estacionamiento',
                [               
                    validators.DataRequired(message = 'Estacionammiento requerido'),
                ],
                    choices=sEstac
                )
    matricula = StringField('Matricula',
                [
                    validators.DataRequired()
                ])
    horaE =  StringField('Hora entrada',[validators.DataRequired()
                ])

    fechaE =  StringField('Fecha entrada',[validators.DataRequired()
                ])

class SalidaForm(Form):
    matricula = StringField('Matricula',
                [
                    validators.DataRequired()
                ])

    horaS = StringField('Hora de salida',
                [ 
                    validators.DataRequired()
                ])
    fechaS = StringField('Fecha de salida',
                [ 
                    validators.DataRequired()
                ])
    horaE = StringField('Hora de entrada',
                [ 
                    validators.DataRequired()
                ])
    fechaE = StringField('Fecha de entrada',
                [
                    validators.DataRequired()
                ]
                )
    total = StringField('Total a pagar',
                [ 
                    validators.DataRequired()
                ])

class RegistroForm(Form):
    nombre = StringField('Estacionamiento',
                [ 
                    validators.DataRequired()
                ])
    direccion = StringField('Dirección',
                [ 
                    validators.DataRequired()
                ])
    telefono = StringField('Telefono',
                [ 
                    validators.DataRequired()
                ])
    capacidad = StringField('Capacidad',
                [ 
                    validators.DataRequired()
                ])
    
    def validate_parking(form, field):
        nombre = field.data
        parking = Estacionamientos.query.filter_by(nombre = nombre).first()
        if parking is not None:
            raise validators.ValidationError('El estacionamiento ya se encuentra registrado!')