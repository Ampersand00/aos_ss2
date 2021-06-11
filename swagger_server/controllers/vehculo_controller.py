import connexion
import flask
from flask.templating import render_template
import six 
import os 
import mysql.connector
# import response
# from flask import make_response,jsonify
from swagger_server.models.http_problem import HTTPProblem
# noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200
# noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001
# noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002
# noqa: E501
from swagger_server.models.vehiculo import Vehiculo
# noqa: E501
from swagger_server import util
from dotenv import load_dotenv
load_dotenv()
HOST = os.getenv('BD_HOST')
USER = os.getenv('BD_USER')
PASS = os.getenv('BD_PASSWORD')
DATABASE = os.getenv('BD_DATABASE')


def taller_clienteId_get(client_id):  # noqa: E501
  # "" "Obtener los vehículos de un cliente concreto.

  #   Permite obtener un vehículo perteneciente a la lista de todos los vehículos de un cliente del taller.  # noqa: E501

  #   : param client_id: ID del cliente.
  #   : type client_id: int

  #   : rtype: InlineResponse2001
  #   " ""
  cnx = mysql.connector.connect(
      user=USER, password=PASS, host=HOST, database=DATABASE)
  cursor = cnx.cursor()
  query = ("SELECT * FROM vehiculos WHERE clienteId=%s;")
  cursor.execute(query, (client_id,))
  a = cursor.fetchall()
  data = []
  for result in a:
   data.append(Vehiculo(result[0], result[1], result[2],
               result[3], result[4], result[5], result[6], result[7]))
  cursor.close()
  cnx.close()
  return data


def taller_matricula_get(matricula):
# noqa: E501
  # "" "Obtener un vehículo concreto a partir de su matrícula

  #   Permite obtener un vehículo perteneciente a la lista de todos los vehículos del taller indicando la matrícula del vehículo.  # noqa: E501

  #   : param matricula: Matrícula del vehículo
  #   : type matricula: str

  #   : rtype: InlineResponse200
  #   " ""
    cnx = mysql.connector.connect(
        user=USER, password=PASS, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    query = ("SELECT * FROM vehiculos WHERE matricula=%s;")
    cursor.execute(query, (matricula,))
    a = cursor.fetchall()
    data = []
    for result in a:
      data.append(Vehiculo(result[0], result[1], result[2],
                  result[3], result[4], result[5], result[6], result[7]))
    cursor.close()
    cnx.close()
    return data


def taller_vehiculo_cget():
# noqa: E501
    # "" "Obtener la lista de vehículos.

    # Permite obtener la lista de todos los vehículos del taller.  # noqa: E501

    # : rtype: InlineResponse200
    # " ""
  cnx = mysql.connector.connect(user=USER, password=PASS,host=HOST,database=DATABASE)
  cursor = cnx.cursor()
  query=("SELECT * FROM vehiculos;")
  cursor.execute(query)
  a=cursor.fetchall()
  data=[]
  for result in a:
    data.append(Vehiculo(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7]))
  cursor.close()
  cnx.close()
  return data
  # a = []
  # a = [USER, PASS, HOST, DATABASE]
  # return a


def taller_vehiculo_options():
# noqa: E501
    # "" "Proporcionar los métodos HTTP soportados para la lista de vehículos.

    # Devuelve una cabecera &#x60;Allow&#x60; con la lista de métodos HTTP soportados (separados por comas). # noqa: E501

    # :rtype: None
    # " ""
# resp=flask.make_response()
# resp.headers['Allow']= "GET, OPTIONS, PUT, DELETE"
# return resp
  resp = flask.make_response(render_template("options"))
  resp.headers['Allow'] = "GET, OPTIONS, PUT, DELETE"
  return resp


def taller_vehiculo_post(body):
# noqa: E501
  # "" "Registrar un nuevo vehículo en el taller.

  #   Genera un nuevo vehículo para añadir a la lista de vehículos gestionados por el taller. # noqa: E501

  #   :param body: &#x60;Vehiculo&#x60; data
  #   :type body: dict | bytes

  #   :rtype: Vehiculo
  #   " ""
    _clienteId = body['clienteId']
    _matricula = body['matricula']
    _marca = body['marca']
    _modelo = body['modelo']
    _color = body['color']
    _anio = body['año']
    _vin = body['VIN']
    cnx = mysql.connector.connect(
        user=USER, password=PASS, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    query = ("INSERT INTO vehiculos(clienteID,matricula,marca,modelo,color,anio,VIN) VALUES(%s,%s, %s, %s, %s,%s, %s)")
    values = (_clienteId, _matricula, _marca, _modelo, _color, _anio, _vin)
    cursor.execute(query, values)
    cnx.commit()
    select = ("SELECT * FROM vehiculos WHERE id=%s")
    cursor.execute(select, (cursor.lastrowid,))
    b = cursor.fetchone()
    result = []
    result.append(Vehiculo(b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7]))
    cursor.close()
    cnx.close()
    return result


def taller_vehiculoid_delete(vehiculo_id):
# noqa: E501
    # "" "Eliminar un vehículo de la lista.

    # Perimite eliminar un vehículo de la lista de los vehículos gestionados por el taller, utilizando su ID. # noqa: E501

    # :param vehiculo_id: ID del vehículo.
    # :type vehiculo_id: int

    # :rtype: None
    # " ""
    cnx = mysql.connector.connect(
        user=USER, password=PASS, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    select = ("SELECT * FROM vehiculos WHERE id=%s")
    cursor.execute(select, (vehiculo_id,))
    a = cursor.fetchall()
    if not a:
      # if len(a) == 0:
      body = HTTPProblem("https://httpstatuses.com/404", "NOT FOUND",
			  404, "El recurso solicitado no está disponible.", "about:blank")
      response404 = flask.make_response(flask.jsonify(body), 404,)
      response404.headers["Content-Type"] = "application/json"
      return response404
    else:
      query = ("DELETE FROM vehiculos WHERE id=%s")
      cursor.execute(query, (vehiculo_id,))
      cnx.commit()
      cursor.fetchall()
      cursor.close()
      cnx.close()
      response204 = flask.make_response(('El vehículo ha sido eliminado de la lista.', 204))
# response204.headers['description']='El vehículo ha sido eliminado de la lista.'
      return response204


def taller_vehiculoid_get(vehiculo_id):
# noqa: E501
    # "" "Obtener un vehículo concreto.

    # Permite obtener un vehículo perteneciente a la lista de todos los vehículos del taller. # noqa: E501

    # :param vehiculo_id: ID del vehículo.
    # :type vehiculo_id: int

    # :rtype: InlineResponse200
    # " ""
    cnx = mysql.connector.connect(
        user=USER, password=PASS, host=HOST, database=DATABASE)
    cursor = cnx.cursor()
    query = ("SELECT * FROM vehiculos WHERE id=%s")
    cursor.execute(query, (vehiculo_id,))
    a = cursor.fetchone()
    result = Vehiculo(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])
    cursor.close()
    cnx.close()
    return result


def taller_vehiculoid_options(vehiculo_id):
# noqa: E501
    # "" "Proporcionar los métodos HTTP soportados para un único vehículo.

    # Devuelve una cabecera &  # x60;Allow&#x60; con la lista de métodos HTTP soportados (separados por comas). # noqa: E501

    # : param vehiculo_id: ID del vehículo.
    # : type vehiculo_id: int

    # : rtype: None
    #     " ""
        resp = flask.Response("optionsId")
        resp.headers['Allow'] = "GET, OPTIONS, PUT, DELETE"
        return resp


def taller_vehiculoid_put(body, vehiculo_id):
# noqa: E501
    #  "" "Modificar un vehículo de la lista.

    # Permite realizar la modificación de los atributos uno de los vehículos gestionados por el taller, seleccionado mediante su ID. # noqa: E501

    # :param body: &#x60;Vehiculo&#x60; data
    # :type body: dict | bytes
    # :param vehiculo_id: ID del vehículo.
    # :type vehiculo_id: int

    # :rtype: Vehiculo
    # " "" 
    _clienteId = body['clienteId']
    _matricula = body['matricula']
    _marca = body['marca'] 
    _modelo = body['modelo'] 
    _color = body['color'] 
    _anio = body['año'] 
    _vin = body['VIN'] 
    intAnio = int(_anio)
    cnx = mysql.connector.connect (user = USER, password = PASS, host = HOST, database = DATABASE) 
    cursor = cnx.cursor()
    values =(_clienteId,_matricula, _marca, _modelo, _color, intAnio, _vin,vehiculo_id)
    cursor.execute("UPDATE vehiculos SET clienteId=%s,matricula=%s,marca=%s,modelo=%s,color=%s,anio=%s,VIN=%s WHERE id=%s;",
   values)
# cursor.execute(query,values)
    cnx.commit()
    select =("SELECT * FROM vehiculos WHERE id=%s;")
    cursor.execute (select, (vehiculo_id,))
    a = cursor.fetchone()
    cursor.close()
    result =Vehiculo(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])
    cnx.close()
# if connexion.request.is_json:
#body = object.from_dict(connexion.request.get_json())  # noqa: E501
    return result
def taller_vin_get(vin):
# noqa: E501
# "" "Obtener el vehículo con un VIN concreto.

#     Permite obtener un vehículo según su identificador único. # noqa: E501

#     :param vin: Número de identificación del vehículo (Vehicle Identification Number).
#     :type vin: str

#     :rtype: InlineResponse2002
#     " "" 
  cnx = mysql.connector.connect(user = USER, password = PASS, host = HOST, database = DATABASE)
  cursor = cnx.cursor()
  query = ("SELECT * FROM vehiculos WHERE VIN=%s")
  cursor.execute (query, (vin,))
  a = cursor.fetchall()
  data =[]
  for result in a:
    data.append(Vehiculo(result[0], result[1], result[2], result[3], result[4], result[5],
	     result[6], result[7])) 
  cursor.close()
  cnx.close()
  return data
