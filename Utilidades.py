from Data_base import Data_base
from Pais import Pais
from Temperaturas import Temperaturas
import Constantes

class Utilidades:
    """
        Programa que consulta 2 APIs: restcountries y openweathermap. Guardo y consulto información en una base de datos.
        Permito que el usuario pueda utilizar una interfaz gráfica para obtener los datos de las temperaturas de las capitales que él quiera.
    """
    obj_pais = Pais()
    obj_Database: Data_base = None
    obj_Temperaturas: Temperaturas = None

    URL_PAISES_EUROPA: str = Constantes.RESTCOUNTRIES_API_URL

    BDD_user: str = Constantes.BDD_user
    BDD_password: str = Constantes.BDD_password
    BDD_host: str = Constantes.BDD_host
    BDD_port: str = Constantes.BDD_port
    BDD_database_name: str = Constantes.BDD_database_name

    def __init__(self):
        print("creando objeto Utilidades.")
        try:
            self.obj_Database = Data_base(
                user=self.BDD_user, 
                password=self.BDD_password, 
                host=self.BDD_host, 
                port=self.BDD_port, 
                database=self.BDD_database_name
            )
        except Exception as e:
            print("Excepción encontrada en el constructor de Utilidades.py:\n")
        
        self.obj_Temperaturas = Temperaturas()

    def main(self):
        """
            Método main que obtiene los datos de los países europeos, las temperaturas de los paises
            y los almacena en la base de datos.
        """
        paises_europeos: list
        temperaturas_de_capitales: list[Temperaturas]
        
        # Obtengo los datos de los paises de la BDD
        paises_europeos = self.obtener_paises_europeos()

        # Consulto a la API para obtener las temperaturas de los paises
        temperaturas_de_capitales = self.obj_Temperaturas.extraer_temperaturas_from_pais(paises_europeos)
        self.insertar_datos_tabla_temperaturas(temperaturas_de_capitales)

        return None

    def obtener_paises_europeos(self):
        """
            Intento obtener los paises europeos de la BDD.
            Si no hay, hago petición a la API y hago inserts en la tabla paises y fronteras.
        """
        # Consulto a la BDD si hay paises europeos
        paises_europeos = self.obj_Database.select_from_table(consulta="SELECT * FROM PAISES")

        # Si no estan en la BDD, mando petición a la API e inserto datos en paises y fronteras
        if len(paises_europeos) == 0:
            paises_europeos = self.obj_pais.obtener_datos_de_paises(self.URL_PAISES_EUROPA)
            self.insertar_datos_tabla_paises(paises_europeos)
            self.insertar_datos_tabla_fronteras(paises_europeos)

        paises_europeos = self.obj_Database.select_from_table(consulta="SELECT * FROM PAISES")

        return paises_europeos

    def insertar_datos_tabla_paises(self, lista_objetos: list[Pais]) -> None:
        for objeto_a_insertar in lista_objetos:
            consulta = self._generar_insert_tabla_paises(objeto_a_insertar)
            self.obj_Database.insert_into_table(consulta)

        return None
    
    def insertar_datos_tabla_fronteras(self, lista_objetos: list[Pais]) -> None:
        """
            Recorro los objetos Pais de list[Pais], creo una consulta que devuelva todos los ID_PAIS de la BDD.
                Recorro el atributo fronteras de cada objeto pais del for anterior.
                    Obtengo el id del pais de la BDD
                    Genero una consulta con ese ID_PAIS y la frontera actual
                    Ejecuto insert en la BDD

            @return None
        """
        for objeto_a_insertar in lista_objetos:
            consulta = f"""SELECT ID_PAIS FROM PAISES WHERE NOMBRE = "{objeto_a_insertar.nombre}"; """
            
            for frontera in objeto_a_insertar.fronteras:
                id_pais_tupla = self.obj_Database.select_from_table(consulta)[0]
                id_pais = id_pais_tupla[0]
                
                consulta_insert = self._generar_insert_tabla_fronteras(id_pais, frontera)
                self.obj_Database.insert_into_table(consulta_insert)
            
        return None
    
    def insertar_datos_tabla_temperaturas(self, lista_temperaturas: list[Temperaturas]) -> None:
        for objeto_a_insertar in lista_temperaturas:
            consulta = self._generar_insert_tabla_temperaturas(objeto_a_insertar)
            self.obj_Database.insert_into_table(consulta)
        
        return None
    
    # ================================================
    # ================Métodos privados================
    # ================================================
    def _generar_insert_tabla_paises(self, obj_pais: Pais) -> str:
        pertenece_UE: int = 0

        if obj_pais.pertenece_a_UE is True:
            pertenece_UE = 1

        consulta: str = "INSERT INTO PAISES (NOMBRE, CAPITAL, REGION, SUBREGION, CCA2, CCA3, MIEMBRO_UE)" \
            "VALUES(" \
                f"'{obj_pais.nombre}'," \
                f"'{obj_pais.capital}'," \
                f"'{obj_pais.region}'," \
                f"'{obj_pais.subregion}'," \
                f"'{obj_pais.cca2}'," \
                f"'{obj_pais.cca3}'," \
                f"{pertenece_UE}" \
            ");"

        return consulta
    
    def _generar_insert_tabla_fronteras(self, id_pais: int, frontera: str) -> str:
        consulta = f"""INSERT INTO FRONTERAS (ID_PAIS, CCA3_FRONTERA) VALUES({id_pais}, "{frontera}");"""
        
        return consulta

    
    def _generar_insert_tabla_temperaturas(self, objeto_a_insertar: Temperaturas) -> str:
        consulta: str = "INSERT INTO TEMPERATURAS (ID_PAIS, TEMPERATURA, SENSACION_TERMICA, MINIMA, MAXIMA, HUMEDAD, HORA_AMANECER, HORA_ATARDECER)" \
            "VALUES(" \
                f"{objeto_a_insertar.id_pais}," \
                f"{objeto_a_insertar.temperatura}," \
                f"{objeto_a_insertar.sensacion_termica}," \
                f"{objeto_a_insertar.minima}," \
                f"{objeto_a_insertar.maxima}," \
                f"{objeto_a_insertar.humedad}," \
                f"{objeto_a_insertar.hora_amanecer}," \
                f"{objeto_a_insertar.hora_atarceder}" \
            ");"

        return consulta

    # Fin clase
