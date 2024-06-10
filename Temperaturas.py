import requests
import Pais as Pais
from datetime import datetime, timezone


class Temperaturas:
    OPENWEATHERMAP_API_URL = "https://api.openweathermap.org/data/2.5/"
    OPENWEATHERMAP_API_KEY = "a60fef3fc371c50c0c57c17361925fad"

    id_pais: int = 0
    temperatura: int = ""
    sensacion_termica: int = ""
    minima: float = 0.0
    maxima: float = 0.0
    humedad: float = 0.0
    hora_amanecer: str = ""
    hora_atarceder: str = ""

    def __init__(self, id_pais=None, temperatura=None, sensacion_termica=None, minima=None, maxima=None, humedad=None, hora_amanecer=None, hora_atarceder=None):
        self.id_pais = id_pais
        self.temperatura = temperatura
        self.sensacion_termica = sensacion_termica
        self.minima = minima
        self.maxima = maxima
        self.humedad = humedad
        self.hora_amanecer = hora_amanecer
        self.hora_atarceder = hora_atarceder
    
    def __str__(self) -> str:
        return f"{self.id_pais},{self.temperatura},{self.sensacion_termica},{self.minima},{self.maxima},{self.humedad},{self.hora_amanecer},{self.hora_atarceder}"
    
    def obtener_obj_en_lista(self):
        """Retornar el objeto Temperaturas en una lista de valores"""
        return [
            self.id_pais,
            self.temperatura,
            self.sensacion_termica,
            self.minima,
            self.maxima,
            self.humedad,
            self.hora_amanecer,
            self.hora_atarceder
        ]
    

    def peticion_api_temperaturas(self, capital):
        return_value: str = ""
        url: str = f"{self.OPENWEATHERMAP_API_URL}weather?q={capital}&appid={self.OPENWEATHERMAP_API_KEY}"

        try:
            return_value = requests.get(url).json()
        
        except Exception as e:
            exit(e)
        
        finally:
            return return_value


    def extraer_temperaturas_from_pais(self, datos_paises: list[Pais]) -> list['Temperaturas']:
        datos_capitales: list[int, str]
        lista_obj_temperaturas = list[Temperaturas]

        datos_capitales = self._obtener_id_pais_y_capital(datos_paises)
        lista_obj_temperaturas = self._obtener_datos_de_capitales(datos_capitales)
        
        return lista_obj_temperaturas
    
    # ================================================
    # ================Métodos privados================
    # ================================================
    
    def _obtener_id_pais_y_capital(self, datos_paises: list[Pais]) -> list[int, str]:
        capitales: list[int, str] = []

        for pais in datos_paises:
            lista_aux = [pais[0], pais[2]]
            capitales.append(lista_aux)

        return capitales
    
    def _obtener_datos_de_capitales(self, datos_capitales: list[int, str]) -> list['Temperaturas']:
        lista_temperaturas = list = []

        for pais in datos_capitales:
            id_pais = pais[0]
            nombre_pais = pais[1]
            
            try:
                aux = self.peticion_api_temperaturas(nombre_pais)
                aux = self._formatear_datos_temperaturas(id_pais, aux)
                
                lista_temperaturas.append(aux)

            except Exception as e:
                print(f"Excepción en Temperaturas.py _obtener_datos_de_capitales(): Posiblemente no se recojan datos del pais '{pais[1]}'")
            
        return lista_temperaturas
    
    def _formatear_datos_temperaturas(self, id_pais: int, datos_temperaturas: dict):
        obj_temperatura: Temperaturas = None

        temperatura: int = datos_temperaturas["main"]["temp"]
        sensacion_termica: int = datos_temperaturas["main"]["feels_like"]
        minima: float = datos_temperaturas["main"]["temp_min"]
        maxima: float = datos_temperaturas["main"]["temp_max"]
        humedad: float = datos_temperaturas["main"]["humidity"]
        hora_amanecer: str = f"""'{self._convertir_unix_a_hora(datos_temperaturas["sys"]["sunrise"])}'"""
        hora_atarceder: str = f"""'{self._convertir_unix_a_hora(datos_temperaturas["sys"]["sunset"])}'"""

        obj_temperatura = Temperaturas(id_pais, temperatura, sensacion_termica, minima, maxima, humedad, hora_amanecer, hora_atarceder)
        
        return obj_temperatura
    
    def _convertir_unix_a_hora(self, unix_timestamp):
        """
        Convierto el valor de unix_timestamp (numero de segundos desde 01/01/1970 hasta hoy) a un formato
        entendible por humanos hora:minuto:segundo
        """
        dt = datetime.utcfromtimestamp(unix_timestamp).replace(tzinfo=timezone.utc)
        return_value = dt.strftime('%H:%M:%S')

        return return_value
