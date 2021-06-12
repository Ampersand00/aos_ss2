# Especificación del Subsistema 2: Vehículos

Integrantes del grupo:
- Miriam Guindel Gómez
- Daniel Martín Fernández 
- Luis Rodríguez Arriero
- Aldara Sacristán Díaz
- Callista Spiteri

<br>

[Enlace a la imagen del Subsistema 2](https://hub.docker.com/r/mguindel/aos_subsistema2)

<br>

## Introducción
Este repositorio contiene los archivos necesarios para poner en marcha un servidor de nuestro subsistema, con el que se podrá interactuar a través de la interfaz de su especificación en Swagger UI. El servidor está basado en Python, utilizando Flask. El código se ha generado mediante la herramienta de [Swagger Codegen](https://github.com/swagger-api/swagger-codegen).

Por otra parte, nuestro servidor también está preparado para acceder a una base de datos persistente de MySQL, utilizando el driver de Python [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/).

Esta documentación contiene información acerca de cómo se estructura la especificación, así como las instrucciones para la puesta en marcha del servidor y de la interfaz de la especificación.

<br>

## Especificación OpenAPI

Para la especificación de la primera parte de la práctica, generamos un sistema de directorios para separar cada uno de los componentes del archivo principal de la especificación, con el fin de facilitar la detección de errores y el trabajo en paralelo. Sin embargo, para el desarrollo de esta segunda parte, así como para generar el código del servidor de Python-Flask, optamos por unificar todos los componentes en un único archivo, "swagger.yaml", contenido en la carpeta "swagger" del proyecto.

Este subsistema contiene los siguientes métodos para gestionar los vehículos del taller:

- **GET (api/v1/vehiculo)**: Devuelve la lista con todos los vehículos del taller, incluyendo tanto los que están en ese momento en el taller como los que hayan estado anteriormente o vayan a entrar en un futuro. Hemos decidido implementar este método para que los empleados del taller puedan obtener una lista completa con todos los vehículos del taller y sus características.

- **POST (api/v1/vehiculo)**: Permite introducir un nuevo vehículo en el sistema del taller. Para ello, será necesario especificar las características del vehículo. Una vez introducido, será posible acceder al vehículo mediante otros métodos del subsistema.

- **OPTIONS (api/v1/vehiculo)**: Devuelve una lista con los métodos del subsistema permitidos si no introducimos ningún parámetro. Este método devuelve los métodos permitidos en una cabecera de tipo `Allow`. Esto permite a los empleados del taller consultar rápidamente las funcionalidades del subsistema.

- **GET (api/v1/vehiculo/{vehiculoId})**: Permite seleccionar un vehículo concreto del sistema utilizando el atributo de `vehiculoId`. Hemos decidido incluir varias opciones de búsqueda mediante GET utilizando distintos atributos, de manera que los empleados del taller puedan acceder a los vehículos que necesiten en cada momento. La búsqueda mediante `vehiculoId` permite seleccionar un único vehículo específico.

- **PUT (api/v1/vehiculo/{vehiculoId})**: Permite modificar los atributos de un vehículo seleccionado mediante el atributo `vehiculoId`. Hemos decidido utilizar el atributo `VIN` por el motivo comentado en el método anterior.

- **OPTIONS (api/v1/vehiculo/{vehiculoId})**: Devuelve una lista con los métodos del subsistema permitidos para un vehículo concreto seleccionado mediante su ID.  Este método devuelve los métodos permitidos en una cabecera de tipo `Allow`. Esto permite a los empleados del taller consultar rápidamente las acciones posibles para un vehículo.

- **DELETE (api/v1/vehiculo/{vehiculoId})**: Permite eliminar un vehículo concreto de la lista de vehículos gestionados por el taller, utilizando el ID del vehículo.

- **GET (api/v1/vehiculo/clientId/{clientId})**: Permite seleccionar una lista con todos los vehículos gestionados por el taller de un cliente concreto, utilizando el atributo `clientId`. Hemos decidido introducir la búsqueda mediante `clientId` para que los empleados puedan acceder a un vehículo conociendo el identificador de la persona que lo llevó al taller, o bien para consultar todos los vehículos de un cliente.

- **GET (api/v1/vehiculo/VIN/{VIN})**: Permite seleccionar un vehículo mediante su número VIN. Hemos decidido introducir la búsqueda mediante `VIN`, ya que generalmente será más sencillo para los empleados del sistema conocer el VIN del vehículo que su Id.

- **GET (api/v1/vehiculo/matricula/{matricula})**: Permite seleccionar un vehículo mediante su matrícula. Hemos decidido introducir la búsqueda mediante `matricula`, ya que en la mayoría de los casos será más fácil buscar un coche por su matrícula que por cualquier otro atributo.

<br>

Los objetos de tipo Vehiculo siguen el esquema:
- **id**: El identificador único del vehículo. Es de tipo número entero. No se puede cambiar tras la creación de un vehículo por lo que hemos decidido incluir la etiqueta `readOnly: "true"`.

- **clientId**: El identificador único del cliente. Es de tipo número entero. Permite asociar un vehículo con el cliente que ha llevado el vehículo al taller. 

- **matricula**: Matrícula del vehículo. Es de tipo string. Inicialmente consideramos darle un formato concreto de cuatro cifras y tres letras. Sin embargo, descartamos este patrón para permitir la compatibilidad con otros formatos de matrículas.

- **marca**: La marca del vehículo. Es de tipo string.
    
- **modelo**: El modelo específico del vehículo. Es de tipo string.

- **color**: El color del vehículo. Es de tipo string. Hemos decidido incluir este atributo porque el color puede suponer una ayuda visual a la hora de localizar rápidamente un vehículo en el taller.

- **año**: El año de fabricación del vehículo. Es de tipo número entero. Sigue el formato `[0-9]{4}`, es decir, cuatro cifras el 0 al 9. Hemos decidido incluir este atributo ya que puede resultar útil para conocer de antemano las diferencias en de los componentes entre vehículos del mismo modelo, pero distinto año.

- **VIN**: El Número de Identificación del Vehículo (Vehicle Identification Number). Es de tipo string, pero únicamente puede contener cifras numéricas y letras. Hemos decidido incluir este atributo ya que incluye mucha información que puede ser útil a la hora de reparar o modificar el vehículo, como el año, el modelo, el tamaño del motor o la fábrica en la que se hizo el vehículo. Aunque incluya información redundante con otros atributos que hemos introducido (como el año o el modelo), hemos preferido incluirlos también para poder acceder a esta información de forma más inmediata.

<br>

## Instrucciones para desplegar el servidor
En primer lugar, puesto que este servidor está basado en Python, es necesario asegurarse de que tenemos **Python 3.5.2** o una versión superior. 

A continuación, deberemos crear la base de datos del subsistema. Hemos incluido en el repositorio un archivo para importar la base de datos de MySQL utilizando PHPMyAdmin. Sin embargo, también se puede crear una nueva base de datos, asegurándose de que existe al menos un usuario con permisos de administrador para esa base de datos y modificar las variables de entorno.

En el caso de crear una nueva base de datos, será necesario modificar el archivo ".env" con los parámetros de ésta: Nombre de la base de datos, nombre y contraseña del usuario, y el puerto a través del cual se deberá conectar el servidor.

Una vez realizados estos pasos, será necesario ejecutar los siguientes comandos desde dentro de la carpeta del proyecto:

```
pip3 install -r requirements.txt
python3 -m swagger_server
```

Finalmente, para acceder a la interfaz de la especificación, será necesario acceder, a través del navegador, a la dirección:

```
http://localhost:8080/api/v1/ui/
```




