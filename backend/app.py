from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)
app.debug=True
CORS(app)

#Creamos las clases que vendran a ser las tablas

# ...

# Tabla empleado
class Empleado(db.Model):
    __tablename__ = 'empleado'

    rut_empleado = db.Column(db.Integer, primary_key=True)
    nom_empleado = db.Column(db.String(50), nullable=False)
    apellido_empleado = db.Column(db.String(50), nullable=False)
    edad_empleado = db.Column(db.Integer, nullable=False)
    maneja = db.Column(db.Boolean, nullable=False)
    celular_empleado = db.Column(db.String(11), nullable=True)
    mail_empleado = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_empleado = db.Column(db.String(50), nullable=False)
    num_cuenta = db.Column(db.Integer, nullable=True)

    def jsonEmpleado(self):
        return {
            'rut_empleado': self.rut_empleado,
            'nom_empleado': self.nom_empleado,
            'apellido_empleado': self.apellido_empleado,
            'edad_empleado': self.edad_empleado,
            'maneja': self.maneja,
            'celular_empleado': self.celular_empleado,
            'mail_empleado': self.mail_empleado,
            'contrasena_empleado': self.contrasena_empleado,
            'num_cuenta': self.num_cuenta
        }

# Tabla empleador
class Empleador(db.Model):
    __tablename__ = 'empleador'

    rut_empleador = db.Column(db.Integer, primary_key=True)
    nom_empleador = db.Column(db.String(50), nullable=False)
    apellido_empleador = db.Column(db.String(50), nullable=False)
    mail_empleador = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_empleador = db.Column(db.String(50), nullable=False)
    celular_empleador = db.Column(db.String(50), nullable=True)

    def jsonEmpleador(self):
        return {
            'rut_empleador': self.rut_empleador,
            'nom_empleador': self.nom_empleador,
            'apellido_empleador': self.apellido_empleador,
            'mail_empleador': self.mail_empleador,
            'contrasena_empleador': self.contrasena_empleador,
            'celular_empleador': self.celular_empleador
        }

# Tabla trabajo
class Trabajo(db.Model):
    __tablename__ = 'trabajo'

    id_trabajo = db.Column(db.Integer, primary_key=True)
    rut_empleador1 = db.Column(db.Integer, db.ForeignKey('empleador.rut_empleador'), nullable=False)
    empleador = db.relationship('Empleador', backref='trabajos')
    nom_trabajo = db.Column(db.String(50), nullable=False)
    descripcion_trabajo = db.Column(db.String(10000), nullable=True)
    estado_trabajo = db.Column(db.String(50), nullable=False)
    fecha_comienzo = db.Column(db.Date, nullable=True)
    fecha_final = db.Column(db.Date, nullable=True)
    pago = db.Column(db.Integer, nullable=False)

    def jsonTrabajo(self):
        return {
            'id_trabajo': self.id_trabajo,
            'rut_empleador1': self.rut_empleador1,
            'nom_trabajo': self.nom_trabajo,
            'descripcion_trabajo': self.descripcion_trabajo,
            'estado_trabajo': self.estado_trabajo,
            'fecha_comienzo': self.fecha_comienzo,
            'fecha_final': self.fecha_final,
            'pago': self.pago
        }

# Tabla empleado_trabajo
class EmpleadoTrabajo(db.Model):
    __tablename__ = 'empleado_trabajo'

    id = db.Column(db.Integer, primary_key=True)
    rut_empleado1 = db.Column(db.Integer, db.ForeignKey('empleado.rut_empleado'), nullable=False)
    empleado = db.relationship('Empleado', backref='trabajos_asignados')
    id_trabajo1 = db.Column(db.Integer, db.ForeignKey('trabajo.id_trabajo'), nullable=False)
    trabajo = db.relationship('Trabajo', backref='empleados_asignados')

    def jsonEmpleadoTrabajo(self):
        return {
            'id': self.id,
            'rut_empleado1': self.rut_empleado1,
            'id_trabajo1': self.id_trabajo1
        }

# ...

db.create_all()


#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# EMPLEADO
@app.route('/empleado', methods=['POST'])
def crear_empleado():
    try:
        data = request.get_json()
        new_empleado = Empleado(
            rut_empleado=data['rut_empleado'],
            nom_empleado=data['nom_empleado'],
            apellido_empleado=data['apellido_empleado'],
            edad_empleado=data['edad_empleado'],
            maneja=data['maneja'],
            celular_empleado=data['celular_empleado'],
            mail_empleado=data['mail_empleado'],
            contrasena_empleado=data['contrasena_empleado'],
            num_cuenta=data.get('num_cuenta', None)  # En caso de que no sea obligatorio
        )
        db.session.add(new_empleado)
        db.session.commit()
        return make_response(jsonify({'message': 'empleado created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating empleado'}), 500)

@app.route('/empleado', methods=['GET'])
def get_all_empleados():
    try:
        empleados = Empleado.query.all()
        empleado_data = [empleado.jsonEmpleado() for empleado in empleados]
        if len(empleado_data) == 0:
            return make_response(jsonify({'message': 'no empleados found'}), 404)
        return make_response(jsonify(empleado_data), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting empleados'}), 500)

@app.route('/empleado/<int:rut_empleado>', methods=['GET'])
def get_empleado(rut_empleado):
    try:
        empleado = Empleado.query.filter_by(rut_empleado=rut_empleado).first()
        if empleado:
            return make_response(jsonify({'empleado': empleado.jsonEmpleado()}), 200)
        return make_response(jsonify({'message': 'empleado not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting empleado'}), 500)

@app.route('/empleado/<int:rut_empleado>', methods=['PUT'])
def update_empleado(rut_empleado):
    try:
        empleado = Empleado.query.filter_by(rut_empleado=rut_empleado).first()
        if empleado:
            data = request.get_json()
            empleado.nom_empleado = data['nom_empleado']
            empleado.apellido_empleado = data['apellido_empleado']
            empleado.edad_empleado = data['edad_empleado']
            empleado.maneja = data['maneja']
            empleado.celular_empleado = data['celular_empleado']
            empleado.mail_empleado = data['mail_empleado']
            empleado.contrasena_empleado = data['contrasena_empleado']
            empleado.num_cuenta = data.get('num_cuenta', None)
            db.session.commit()
            return make_response(jsonify({'message': 'empleado updated'}), 200)
        return make_response(jsonify({'message': 'empleado not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating empleado'}), 500)

@app.route('/empleado/<int:rut_empleado>', methods=['DELETE'])
def delete_empleado(rut_empleado):
    try:
        empleado = Empleado.query.filter_by(rut_empleado=rut_empleado).first()
        if empleado:
            db.session.delete(empleado)
            db.session.commit()
            return make_response(jsonify({'message': 'empleado deleted'}), 200)
        return make_response(jsonify({'message': 'empleado not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting empleado'}), 500)
    


# EMPLEADOR
@app.route('/empleador', methods=['POST'])
def crear_empleador():
    try:
        data = request.get_json()
        new_empleador = Empleador(
            rut_empleador=data['rut_empleador'],
            nom_empleador=data['nom_empleador'],
            apellido_empleador=data['apellido_empleador'],
            mail_empleador=data['mail_empleador'],
            contrasena_empleador=data['contrasena_empleador'],
            celular_empleador=data['celular_empleador']
        )
        db.session.add(new_empleador)
        db.session.commit()
        return make_response(jsonify({'message': 'empleador created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating empleador'}), 500)

@app.route('/empleador', methods=['GET'])
def get_all_empleadores():
    try:
        empleadores = Empleador.query.all()
        empleador_data = [empleador.jsonEmpleador() for empleador in empleadores]
        if len(empleador_data) == 0:
            return make_response(jsonify({'message': 'no empleadores found'}), 404)
        return make_response(jsonify(empleador_data), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting empleadores'}), 500)

@app.route('/empleador/<int:rut_empleador>', methods=['GET'])
def get_empleador(rut_empleador):
    try:
        empleador = Empleador.query.filter_by(rut_empleador=rut_empleador).first()
        if empleador:
            return make_response(jsonify({'empleador': empleador.jsonEmpleador()}), 200)
        return make_response(jsonify({'message': 'empleador not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting empleador'}), 500)

@app.route('/empleador/<int:rut_empleador>', methods=['PUT'])
def update_empleador(rut_empleador):
    try:
        empleador = Empleador.query.filter_by(rut_empleador=rut_empleador).first()
        if empleador:
            data = request.get_json()
            empleador.nom_empleador = data['nom_empleador']
            empleador.apellido_empleador = data['apellido_empleador']
            empleador.celular_empleador = data['celular_empleador']
            empleador.mail_empleador = data['mail_empleador']
            empleador.contrasena_empleador = data['contrasena_empleador']
            db.session.commit()
            return make_response(jsonify({'message': 'empleador updated'}), 200)
        return make_response(jsonify({'message': 'empleador not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating empleador'}), 500)

@app.route('/empleador/<int:rut_empleador>', methods=['DELETE'])
def delete_empleador(rut_empleador):
    try:
        empleador = Empleador.query.filter_by(rut_empleador=rut_empleador).first()
        if empleador:
            db.session.delete(empleador)
            db.session.commit()
            return make_response(jsonify({'message': 'empleador deleted'}), 200)
        return make_response(jsonify({'message': 'empleador not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting empleador'}), 500)



# TRABAJO
@app.route('/trabajo', methods=['POST'])
def crear_trabajo():
    try:
        data = request.get_json()
        new_trabajo = Trabajo(
            id_trabajo=data["id_trabajo"],
            nom_trabajo=data['nom_trabajo'],
            descripcion_trabajo=data['descripcion_trabajo'],
            pago=data['pago'],
            fecha_comienzo=data['fecha_comienzo'],
            fecha_final=data['fecha_final'],
            rut_empleador1=data['rut_empleador'],
            estado_trabajo=data['estado_trabajo']
        )
        db.session.add(new_trabajo)
        db.session.commit()
        return make_response(jsonify({'message': 'trabajo created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating trabajo'}), 500)



# Obtener todos los trabajos
@app.route('/trabajo', methods=['GET'])
def get_all_trabajos():
    try:
        trabajos = Trabajo.query.all()
        trabajo_data = [trabajo.jsonTrabajo() for trabajo in trabajos]
        
        if len(trabajo_data) == 0:
            return make_response(jsonify({'message': 'no trabajos found'}), 404)
        
        return make_response(jsonify(trabajo_data), 200)

    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'error getting trabajos'}), 500)

# Obtener trabajo por id_trabajo
@app.route('/trabajo/<int:id_trabajo>', methods=['GET'])
def get_trabajo(id_trabajo):
    try:
        trabajo = Trabajo.query.filter_by(id_trabajo=id_trabajo).first()
        if trabajo:
            return make_response(jsonify({'trabajo': trabajo.jsonTrabajo()}), 200)
        return make_response(jsonify({'message': 'trabajo not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error getting trabajo'}), 500)

# Actualizar trabajo
@app.route('/trabajo/<int:id_trabajo>', methods=['PUT'])
def update_trabajo(id_trabajo):
    try:
        trabajo = Trabajo.query.filter_by(id_trabajo=id_trabajo).first()
        if trabajo:
            data = request.get_json()
            trabajo.rut_empleador1 = data.get('rut_empleador1', trabajo.rut_empleador1)
            trabajo.nom_trabajo = data.get('nom_trabajo', trabajo.nom_trabajo)
            trabajo.descripcion_trabajo = data.get('descripcion_trabajo', trabajo.descripcion_trabajo)
            trabajo.estado_trabajo = data.get('estado_trabajo', trabajo.estado_trabajo)
            trabajo.fecha_comienzo = data.get('fecha_comienzo', trabajo.fecha_comienzo)
            trabajo.fecha_final = data.get('fecha_final', trabajo.fecha_final)
            trabajo.pago = data.get('pago', trabajo.pago)
            
            db.session.commit()
            return make_response(jsonify({'message': 'trabajo updated'}), 200)
        return make_response(jsonify({'message': 'trabajo not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error updating trabajo'}), 500)

# Borrar trabajo
@app.route('/trabajo/<int:id_trabajo>', methods=['DELETE'])
def delete_trabajo(id_trabajo):
    try:
        trabajo = Trabajo.query.filter_by(id_trabajo=id_trabajo).first()
        if trabajo:
            db.session.delete(trabajo)
            db.session.commit()
            return make_response(jsonify({'message': 'trabajo deleted'}), 200)
        return make_response(jsonify({'message': 'trabajo not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error deleting trabajo'}), 500)


# EMPLEADOTRABAJO
@app.route('/empleadotrabajo', methods=['POST'])
def crear_empleadotrabajo():
    try:
        data = request.get_json()
        new_empleadotrabajo = EmpleadoTrabajo(
            rut_empleado=data['rut_empleado'],
            id_trabajo=data['id_trabajo'],
            estado=data['estado']
        )
        db.session.add(new_empleadotrabajo)
        db.session.commit()
        return make_response(jsonify({'message': 'empleadotrabajo created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error creating empleadotrabajo'}), 500)

# Similarmente, agregarías las funciones get_all_empleadotrabajos, get_empleadotrabajo, update_empleadotrabajo, y delete_empleadotrabajo.



