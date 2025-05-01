import sqlite3
from tkinter import *
from tkinter import messagebox as MessageBox

""""
Para crear las funciones que usaré regularmente para consultar la base de datos.
Consulta, registro, eliminación
"""

def name_database(self): # Definicion del nombre de la base de datos
    db_name = 'gvdatabases.db'
    self.db_name = db_name

        
def run_query(self, query, parametros=()): # La función de busqueda
    with sqlite3.connect(self.db_name) as conn: # Coneccion
        cursor = conn.cursor() # Cursor
        result = cursor.execute(query, parametros)
        conn.commit()
    return result
    

def get_pedidos(self, pagina): # Para obtener la lista de pedidos
    record = pagina.get_children()
    for element in record:
        pagina.delete(element)

    query = "SELECT idpedido, ganancia FROM Pedidos ORDER BY idpedido DESC"
    db_rows = self.run_query(query)
    for row in db_rows:
        pagina.insert('', 0, text=row[0], values=row[1]+"$")


def get_cal_mensual(self, pagina): # Para obtener la tabla de calculo mensual
    record = pagina.get_children()
    for element in record:
        pagina.delete(element)

    query = "SELECT Fecha, Ingreso, Egreso FROM Negocio ORDER BY Fecha DESC"
    db_rows = self.run_query(query)
    for row in db_rows:
        pagina.insert('', 0, text= row[0])


def get_ing_det(self, pagina): # Tabla de Ingresos y egresos detallados
    record = pagina.get_children()
    for element in record:
        pagina.delete(element)

    query = "SELECT * FROM Negocio ORDER BY id DESC"
    db_rows = self.run_query(query)
    for row in db_rows:
        pagina.insert('', 'end', values=row[:])


def validacion(self):
    return len(self.fecha.get()) != 0 and len(self.detalles.get()) != 0


def cua_limpiar(self):
    self.fecha.delete(0, END)
    self.detalles.delete(0, END)
    self.ingreso.delete(0, END)
    self.egreso.delete(0, END)


def add_evento(self, pagina):
    if validacion(self):
        query = 'INSERT INTO Negocio VALUES (NULL, ?, ?, ?, ?)'
        parametros = (self.fecha.get(), self.detalles.get(), self.ingreso.get(), self.egreso.get())
        new_values = ['0' if x=='' else x for x in parametros]
        self.run_query(query, tuple(new_values))
        self.cua_limpiar()
        self.message['text'] = 'Entrada guardada'
    else:
        self.message['text'] = 'Fecha y Detalles requeridos'
    get_ing_det(self, pagina)


def delete_evento(self, pagina):
    self.message['text'] = ''
    try:
        selected_item = pagina.selection()[0]  # obteniemos el primer item seleccionado
        item_values = pagina.item(selected_item)['values'] # accedemos al valor
        
        respuesta = MessageBox.askokcancel('Verifica eliminación', '¿Seguro que desea eliminar el registro?') # Titulo y mensaje
        if respuesta == True:
            record_id = item_values[0]  # Obtenemos la ID por la tupla
            query = "DELETE FROM Negocio WHERE id = ?" # Usando el ID eliminamos el registro de la database

            self.run_query(query, (record_id,)) # Pasamos la ID como una tupla
            self.message['text'] = 'Evento eliminado del registro'

            get_ing_det(self, pagina)
        else:
            self.message['text'] = 'Registro no eliminado'

    except IndexError:
        self.message['text'] = 'Selecciona un registro primero'
    except Exception as e: # Si Sale otro error
        self.message['text'] = f"Error al eliminar: {e}" # Para que salga en pantalla el error
        print(f"Delete Error: {e}")


def actualizar_evento(self, pagina):
    self.message['text'] = ''
    if validacion(self):
        try:
            selected_item = pagina.selection()[0]  # obteniemos el primer item seleccionado
            old_item = pagina.item(selected_item)['values'] # accedemos al valor
           
            # Ventana para verificar la actualizacion
            respuesta = MessageBox.askokcancel('Verifica actualización', '¿Seguro que desea actualizar el registro?') # Titulo y mensaje
            if respuesta == True:
                old_id = old_item[0]
                old_item_values = old_item[1:]
                parametros = [self.fecha.get(), self.detalles.get(), self.ingreso.get(), self.egreso.get()]
                new_values = ['0' if x=='' else x for x in parametros]
                query = f'UPDATE Negocio SET Fecha=?, Detalles=?, Ingreso=?, Egreso=? WHERE id={old_id}'
                self.run_query(query, tuple(new_values))
                self.cua_limpiar()
                self.message['text'] = 'Entrada Actualizada'
                get_ing_det(self, pagina)
            else:
                self.cua_limpiar()
                self.message['text'] = 'Entrada no actualizada'

        except IndexError:
            self.message['text'] = 'Selecciona un registro primero'
        except Exception as e: # Si Sale otro error
            self.message['text'] = f"Error al actualizar: {e}" # Para que salga en pantalla el error
            print(f"Update Error: {e}")
    else:
        self.message['text'] = 'Fecha y Detalles requeridos'
    get_ing_det(self, pagina)