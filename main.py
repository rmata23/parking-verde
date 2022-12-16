#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for
from flask import render_template, request
from flask import session, flash, g

from flask_wtf import CSRFProtect

from config import DevelopmentConfig

from models import db, User, Entradas
from models import Estacionamientos, Registros

import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in [
        'entradasReg', 'crear', 'añadir', 'verUsuarios', 'verEstacionamientos']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'entrada', 'salida', 'salidab']:
        return redirect(url_for('entradasReg'))

@app.after_request
def after_request(response):
    return response

@app.route('/')
def index():
    title="Bienvenido al estacionamiento"
    
    return render_template('index.html', title=title) 

@app.route('/entrada', methods=['GET', 'POST'])
def entrada():
    entrada_form = forms.EntradaForm(request.form)

    if request.method == 'POST' and entrada_form.validate():
        print  ("Hola")
        entrada = Entradas(matricula= entrada_form.matricula.data,
                           estacionamiento=entrada_form.estacionamiento.data,
                           hora_entrada=entrada_form.horaE.data,
                           fecha_entrada=entrada_form.fechaE.data)
        
        db.session.add(entrada)
        db.session.commit()

        success_message = 'Entrada registrada en la base de datos'
        flash(success_message)

    return render_template('entrada.html', form = entrada_form) 

@app.route('/salida', methods=['GET','POST'])
def salidab():
    salida_form = forms.SalidaForm(request.form)
    
    return render_template('salida1.html', form = salida_form) 

@app.route('/salida/<string:matricula>', methods=['GET','POST'])
def salida(matricula):

    salida_form = forms.SalidaForm(request.form)
    if request.method == 'POST' and salida_form.validate():
        
        salida = Registros(registro_matricula= salida_form.matricula.data,
                           fecha_salida=salida_form.fechaS.data,
                           hora_salida=salida_form.horaS.data,
                           total=salida_form.total.data)
        
        db.session.add(salida)
        db.session.commit()

        success_message = 'Se ha registrado una salida'
        flash(success_message)    
        return redirect(url_for('salidab'))
    
    entrada_list = Entradas.query.filter_by(matricula=matricula).all()   
    if entrada_list is not None:
        if request.method=='POST' and salida_form.validate():
            reSalidas = "Hola"
        return render_template('salida.html', form = salida_form, entrada_list=entrada_list) 
    else:
        return redirect(url_for('salidab'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        user = User.query.filter_by(username = username).first()

        if user is not None and user.verify_password(password):
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            session['username'] = login_form.username.data
            session['user_id'] = user.id
            return redirect(url_for('entradasReg'))
        else:
            error_message = 'Usuario o password no validos!'
            flash(error_message)

        session['username'] = login_form.username.data 
    return render_template('login.html', form = login_form)

@app.route('/registros/', methods= ['GET', 'POST'])
def entradasReg():
    registros_list = Entradas.query.join(Registros).add_columns(
                                            Entradas.id,
                                            Entradas.matricula,
                                            Entradas.estacionamiento,
                                            Entradas.fecha_entrada,
                                            Entradas.hora_entrada,
                                            Registros.fecha_salida,
                                            Registros.hora_salida,
                                            Registros.total)
    return render_template('registros.html', registros_list= registros_list)

@app.route('/crear',  methods = ['GET', 'POST'])
def crear():
    usuarios_form = forms.UsuariosForm(request.form)
    if request.method == 'POST' and usuarios_form.validate():
        user = User( usuarios_form.username.data,
                     usuarios_form.password.data)
        db.session.add(user)
        db.session.commit()

        success_message = 'Usuario registrado en la base de datos'
        flash(success_message)
        return redirect(url_for("verUsuarios"))
        
    return render_template('crear.html', form = usuarios_form) 

@app.route('/usuarios', methods = ['GET'])
def verUsuarios():
    users = User.query.all()
    return render_template('usuarios.html', users = users)

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        success_message = 'Usuario eliminado!'
        flash(success_message)
        return render_template('usuarios.html', user_to_delete = user_to_delete)
    except:
        error_message = 'Whooops! Hubo un error.'
        flash(error_message)
        return render_template('usuarios.html', user_to_delete = user_to_delete)

@app.route('/añadir', methods = ['GET', 'POST'])
def añadir():
    registro_form = forms.RegistroForm(request.form)
    if request.method == 'POST' and registro_form.validate():
        registro = Estacionamientos(nombre = registro_form.nombre.data,
                                    direccion = registro_form.direccion.data,
                                    telefono = registro_form.telefono.data,
                                    capacidad = registro_form.capacidad.data)
        db.session.add(registro)
        db.session.commit()

        success_message = 'Estacionamiento registrado en la base de datos'
        flash(success_message)
        return redirect(url_for("verEstacionamientos"))
    return render_template('añadir.html', form = registro_form)

@app.route('/estacionamientos', methods = ['GET'])
def verEstacionamientos():
    estacionamientos = Estacionamientos.query.all()
    return render_template('estacionamientos.html', estacionamientos = estacionamientos)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    estacionamiento_to_delete = Estacionamientos.query.get_or_404(id)

    try:
        db.session.delete(estacionamiento_to_delete)
        db.session.commit()
        success_message = 'Estacionamiento eliminado!'
        flash(success_message)
        return render_template('estacionamientos.html', estacionamiento_to_delete = estacionamiento_to_delete)
    except:
        error_message = 'Whooops! Hubo un error.'
        flash(error_message)
        return render_template('estacionamientos.html', estacionamiento_to_delete = estacionamiento_to_delete)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('index'))

def sEstac():
   return [(r.nombre, r.nombre) for r in Estacionamientos.query.add_columns(Estacionamientos.nombre)]

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(port = 8000, host='0.0.0.0')
