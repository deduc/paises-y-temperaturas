from flask import Flask, render_template, request
from Utilidades import Utilidades
from Data_base import Data_base
import Constantes


# Configuro el directorio donde voy a obtener las plantillas html de la aplicacion
app = Flask(__name__, template_folder="./templates")


@app.route("/", methods=["GET"])
def main():
    """
        Función que muestra la pagina index.html (contenedora de un formulario)
        y es capaz de devolver unos datos a partir del formulario.

        Se ejecuta cuando el usuario entra en la raíz de la web.
    """
    obj_database: Data_base = Data_base(Constantes.BDD_user, Constantes.BDD_password, Constantes.BDD_host, Constantes.BDD_port, Constantes.BDD_database_name)
    datos_pais_y_temperatura = inicializar_datos(obj_database)

    return render_template("index.html", datos_pais=datos_pais_y_temperatura)


def inicializar_datos(obj_database: Data_base):
    nombre_pais: str = request.args.get(key="pais", default="").upper()
    datos_pais_y_temperatura: dict = {
        "nombre": "", 
        "capital": "", 
        "region": "", 
        "temperatura": "", 
        "minima": "",
        "maxima": "", 
        "amanecer": "", 
        "atardecer": ""
    }

    if len(nombre_pais) > 0:
        # Convierto a list los 2 list[RowType] obtenidos a continuacion

        pais_row: list = obtener_datos_pais(obj_database, nombre_pais)

        if len(pais_row) > 0:
            pais_row: list = list(pais_row[0])
            temperatura_pais = list(obtener_temperaturas_de_pais(obj_database, pais_row[0])[0])
            datos_pais_y_temperatura = formatear_datos_y_temperatura(pais_row, temperatura_pais)


    return datos_pais_y_temperatura



def obtener_datos_pais(obj_database: Data_base, nombre_pais: str):
    """
        Obtengo todos los datos de un pais en concreto y retorno la fila obtenida como resultado
        @return list[RowType]
    """
    consulta = f"SELECT * FROM PAISES WHERE UPPER(NOMBRE) = '{nombre_pais.upper()}'"
    cursor = obj_database.conexion.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchall()

    return resultado


def obtener_temperaturas_de_pais(obj_database: Data_base, id_pais: int) -> list:
    """
        Obtengo las temperaturas de la capital de un pais en concreto y retorno la fila obtenida como resultado
        @return list[RowType]
    """
    consulta = f"SELECT * FROM TEMPERATURAS WHERE ID_PAIS = {id_pais}"
    cursor = obj_database.conexion.cursor()
    cursor.execute(consulta)
    resultado = cursor.fetchall()

    return resultado


def formatear_datos_y_temperatura(datos_pais: list, temperatura_pais: list) -> dict:
    """
        Retorno un diccionario con los datos que quiero obtener a partir de 2 listas que suponen filas de tablas de BDD
        @return dict
    """
    return {
        "nombre": datos_pais[1],
        "capital": datos_pais[2],
        "region": datos_pais[3],
        "temperatura": temperatura_pais[2],
        "minima": temperatura_pais[4],
        "maxima": temperatura_pais[5],
        "amanecer": format_timedelta(temperatura_pais[7]),
        "atardecer": format_timedelta(temperatura_pais[8])
    }


def format_timedelta(td: int) -> str:
    """
        Obtengo un número de segundos en formato unix (segundos desde 01/01/1970) y lo convierto a horas:minutos:segundos
        @return str
    """
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)


def inicializar_aplicacion():
    print("Inicializando la aplicación, espera...")
    # inicializado = True
    utilidades_obj = Utilidades()
    utilidades_obj.main()
    # paises_europeos: list
    # temperaturas_de_capitales: list
    #
    # # Obtengo los datos de los paises de la BDD
    # paises_europeos = utilidades_obj.obtener_paises_europeos()
    #
    # # Consulto a la API para obtener las temperaturas de los paises
    # temperaturas_de_capitales = utilidades_obj.obj_Temperaturas.extraer_temperaturas_from_pais(paises_europeos)
    # utilidades_obj.insertar_datos_tabla_temperaturas(temperaturas_de_capitales)


inicializado = False
if inicializado is False:
    inicializar_aplicacion()
app.run(port=5000)
