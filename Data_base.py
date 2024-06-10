import mysql.connector
import Constantes as ct

class Data_base:
    # Objeto conexion con la BDD
    conexion = None
    
    # Datos de autenticación para conectarse a la BDD
    user: str = ""
    password: str = ""
    host: str = ""
    port: str = ""
    database: str = ""
    
    palabra_especial_select: str = ct.PALABRA_ESPECIAL_SELECT
    palabra_especial_insert: str = ct.PALABRA_ESPECIAL_INSERT
    mensaje_error_consulta_palabra_especial_select: str = ct.MENSAJE_ERROR_CONSULTA_PALABRA_ESPECIAL_SELECT
    mensaje_error_consulta_palabra_especial_insert: str = ct.MENSAJE_ERROR_CONSULTA_PALABRA_ESPECIAL_INSERT
    mensaje_error_sintaxis_select: str = ct.MENSAJE_ERROR_SINTAXIS_SELECT
    mensaje_error_sintaxis_insert: str = ct.MENSAJE_ERROR_SINTAXIS_INSERT
    mensaje_error_buscate_la_vida: str = ct.MENSAJE_ERROR_BUSCATE_LA_VIDA


    def __init__(self, user, password, host, port, database):
        print("Creando objeto Data_base")
        try:
            print("Intentando conectar con la base de datos.")
            self.conexion = self.conectar_con_bbdd(user, password, host, port, database)

            if self.conexion:
                self.user = user
                self.password = password
                self.host = host
                self.port = port
                self.database = database

                print("Conexion establecida con la base de datos.")
            
        except Exception as e:
            print("ERROR: No se ha podido conectar con la base de datos, los valores introducidos no son correctos.")
            print(e)

    def conectar_con_bbdd(self, usuario, password, ip_host, puerto, base_de_datos):
        conexion = None
        
        try:
            conexion = mysql.connector.connect(user=usuario, password=password, host=ip_host, port=puerto, database=base_de_datos)

        except Exception as e:
            print("Excepcion: " + e)

        return conexion
    
    def select_from_table(self, consulta):
        resultado_consulta = []
        
        #* Las consultas select válidas son aquellas que sí o sí empiezan por 'SELECT '.
        self._comprobar_consulta(self.palabra_especial_select, consulta, self.mensaje_error_consulta_palabra_especial_select)
        
        # Comprobar conexiones con la BDD
        if self.conexion and self.conexion.is_connected():
            try:
                # Genero un cursor con el que manipular la BDD y almacenar resultados.
                cursor = self.conexion.cursor()
                cursor.execute(consulta)

                # Obtengo las filas que ha obtenido el cursor
                resultado_consulta = cursor.fetchall()
            
            except Exception as e:
                print(self.mensaje_error_sintaxis_select, e)

        else:
            print(self.mensaje_error_buscate_la_vida)

        return resultado_consulta
    
    def insert_into_table(self, consulta):
        # * Las consultas insert válidas son aquellas que sí o sí empiezan por 'INSERT '.
        self._comprobar_consulta(self.palabra_especial_insert, consulta, self.mensaje_error_consulta_palabra_especial_insert)

        # Comprobar conexiones con la BDD
        if self.conexion and self.conexion.is_connected():
            try:
                # Genero un cursor con el que manipular la BDD y almacenar resultados.
                cursor = self.conexion.cursor()
                cursor.execute(consulta)

                # Confirmo los cambios en la BDD
                self.conexion.commit()

            except Exception as e:
                print(self.mensaje_error_sintaxis_insert, e)

        else:
            print(self.mensaje_error_buscate_la_vida)
    
    def imprimir_resultado_select(self, lista_filas):
        for fila in lista_filas:
            print(fila)
    
    # ================================================
    # ================Métodos privados================
    # ================================================

    def _comprobar_consulta(self, palabra_especial, consulta, mensaje_error):
        if palabra_especial.upper() not in consulta.upper():
            print("Data_base._comprobar_consulta()", consulta, "/n", mensaje_error)
            exit()
    
    # fin clase
