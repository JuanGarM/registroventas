from tkinter import *
from tkinter import ttk
import sqlite3
import gvdatabase
from tkcalendar import DateEntry


class Gorventas():

    db_name = 'gvdatabase.db'

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("Gordiventas")
        self.ventana.geometry('1100x600')
        self.ventana.iconbitmap('imagenes/mmicon.ico')
        self.ventana.config(background="bisque1")
        self.ventana.resizable(0,0)
        
        
        #Panel para las pestañas
        self.pesta = ttk.Notebook(self.ventana)
        self.pesta.pack(fill='both', expand='1')
        self.noteStyle = ttk.Style()
        self.noteStyle.theme_use('default')
        self.noteStyle.configure("TNotebook", background='bisque2') #configuración de las pestañas visual
        self.noteStyle.configure("TNotebook.Tab", background="bisque2", font='arial, 12' ) #Configuración del encabezado donde están las pestañas
        self.noteStyle.map("TNotebook", background=[("selected", 'bisque2')])

        #Color de fondo de las pestañas
        self.noteStyle.configure('mi.TFrame', background='bisque1', relief='sunken')
        
        #Crear pestañas
        p1 = ttk.Frame(self.pesta, style='mi.TFrame')
        p2 = ttk.Frame(self.pesta, style='mi.TFrame')
        p3 = ttk.Frame(self.pesta, style='mi.TFrame')
        p4 = ttk.Frame(self.pesta, style='mi.TFrame')

        #Agregar elementos a las pestañas
        """
        Todos los elemento agregados a las pestañas deben ser definidos antes de agregar las pestañas
        El primer parametro indica la pestaña donde irá el wigeth.
        .grid se usa para delimitar la posición del elemento, sin él, no se muestra en la pantalla.
        puede crearse una variable con la cual luego agregar el .grid 
        """
        #p1, contenido:
        # Registro de Pedidos
        p1_regped = Label(p1, text='Registro de Pedidos', background='bisque1')
        p1_regped.grid(row=0, column=0, columnspan= 2, padx=10, pady=10)
        self.cont_p1= ttk.Treeview(p1, height= 24, columns= (1)) #Me falta colocar el estilo
        self.cont_p1.grid(row=1, column= 0)
        self.cont_p1.heading("#0", text= "Pedido", anchor=CENTER)
        self.cont_p1.heading(1, text= "Ganancia", anchor=CENTER)
        self.cont_p1.column('#0', width=60, anchor=CENTER)
        self.cont_p1.column(1, width=100, anchor=CENTER)

        gvdatabase.get_pedidos(self, self.cont_p1)

        Label(p1, background='bisque1').grid(row=0, column=1)

        # Registro de Ingresos/Egresos por Mes
        p1_rie = Label(p1, text= 'Registro de Ingresos/Egresos por mes', background='bisque1')
        p1_rie.grid(row=0, column=2, columnspan= 2, padx=10, pady=10)
        self.cont2_p1 = ttk.Treeview(p1, height= 24, columns= [1,2])
        self.cont2_p1.grid(row=1, column=2, padx=5)
        self.cont2_p1.heading("#0", text= "Mes", anchor=CENTER)
        self.cont2_p1.heading(1, text= "Ingreso", anchor=CENTER)
        self.cont2_p1.heading(2, text= "Egreso", anchor=CENTER)
        self.cont2_p1.column('#0', width=100, anchor=CENTER)
        self.cont2_p1.column(1, width=120, anchor=CENTER)
        self.cont2_p1.column(2, width=120, anchor=CENTER)
        #self.cont2_p1.insert()
        gvdatabase.get_cal_mensual(self, self.cont2_p1)

        # P2, contenido:
        # Ingresos y Egresos detallados
        ing_det = Label(p2, text='Ingresos Y Egresos detallado', background='bisque1')
        ing_det.grid(row=0, column=0, pady=1, columnspan=2)
        self.cont_p2 = ttk.Treeview(p2, height= 20, columns=[1,2,3,4,5])
        self.cont_p2.grid(row=1, column=0, sticky='nsew')
    
        # Barra desplazamiento
        barra = Scrollbar(p2, orient='vertical', command=self.cont_p2.yview)
        self.cont_p2.config(yscrollcommand=barra.set)
        barra.grid(row=1, column=1, sticky=NS)
        p2.grid_columnconfigure(0, weight=1)
        

        self.cont_p2.heading('#0')
        self.cont_p2.heading(1, text= "ID", anchor=CENTER)
        self.cont_p2.heading(2, text= "Fecha", anchor=CENTER)
        self.cont_p2.heading(3, text= "Detalles", anchor=CENTER)
        self.cont_p2.heading(4, text= "Ingreso", anchor=CENTER)
        self.cont_p2.heading(5, text= "Egreso", anchor=CENTER)

        self.cont_p2.column('#0', width=0)
        self.cont_p2.column(1, width=30, anchor=CENTER)
        self.cont_p2.column(2, width=100, anchor=CENTER)
        self.cont_p2.column(3, width=400, anchor=CENTER)
        self.cont_p2.column(4, width=60, anchor=CENTER)
        self.cont_p2.column(5, width=60, anchor=CENTER)

        gvdatabase.get_ing_det(self, self.cont_p2)

        #Label(p2, background='bisque1').pack()

        #Registro de Eventos
        reg_eventos = Label(p2, text="Registrar", background='bisque1')
        reg_eventos.grid(row=0, column=2, padx=70)


        # Se crea un calendario para ingresarlas sin escribirlas
        cua_fecha = Label(p2, text='Fecha: ', background='bisque3')
        cua_fecha.grid(row=1, column=2, sticky=NW, padx=5)
        self.fecha = DateEntry(p2, selectmode='day', date_pattern='yyyy-mm-dd')
        self.fecha.grid(row=1, column=2, sticky=NW, padx=55)

        # Ingreso
        cua_ingreso = Label(p2, text='Ingreso: ', background='bisque3')
        cua_ingreso.grid(row=1, column=2, sticky=NW, pady= 25, padx= 5)
        self.ingreso = Entry(p2)
        self.ingreso.grid(row=1, column=2, sticky=NW, padx=60, pady= 25)

        # Egreso
        cua_egreso = Label(p2, text='Egreso: ', background='bisque3')
        cua_egreso.grid(row=1, column=2, sticky=NW, pady= 50, padx= 5)
        self.egreso = Entry(p2)
        self.egreso.grid(row=1, column=2, sticky=NW, padx=60, pady= 50)

        # Detalles
        cua_detalles = Label(p2, text='Detalles: ', background='bisque3')
        cua_detalles.grid(row=1, column=2, sticky=NW, pady= 75, padx= 5)
        self.detalles = Entry(p2)
        self.detalles.grid(row=1, column=2, sticky=NW, pady= 75, padx=60, ipadx=40)
        
        # Seleccion de evento en el registro
        def selec_valor(event):
            selected_item = self.cont_p2.selection()[0]  # obteniemos el primer item seleccionado
            old_item = self.cont_p2.item(selected_item)['values'] # accedemos al valor
            self.cua_limpiar()
            self.fecha.set_date(old_item[1])
            self.detalles.insert(0, old_item[2])
            self.ingreso.insert(0, old_item[3])
            self.egreso.insert(0, old_item[4])
        
        self.cont_p2.bind("<Double-Button-1>", selec_valor)

        
        # Botones registro de eventos
        self.guardar = ttk.Button(p2, text='Guardar', command= lambda: gvdatabase.add_evento(self, self.cont_p2))
        self.guardar.grid(row=1, column=2, sticky=NW, pady= 105, padx=50)

        self.eliminar = ttk.Button(p2, text='Eliminar', command= lambda: gvdatabase.delete_evento(self, self.cont_p2))
        self.eliminar.grid(row=1, column=2, sticky=N, pady= 105)

        self.actualizar = ttk.Button(p2, text='Actualizar', command= lambda: gvdatabase.actualizar_evento(self, self.cont_p2))
        self.actualizar.grid(row=1, column=2, sticky=NE, pady= 105, padx=55)

        # Mensaje registro de eventos
        self.message = Label(p2, text= ' ', background='bisque1')
        self.message.grid(row=1, column=2, sticky=N, pady=135)

        #p3, contenido:
        #p4, contenido:


        #Agregar pestañas
        self.pesta.add(p1,text='Ventas general')
        self.pesta.add(p2, text='Ingresos por orden')
        self.pesta.add(p3, text='Pedidos Y Cobros')
        self.pesta.add(p4, text='Comisiones')


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    

    def validacion(self):
        return len(self.fecha.get()) != 0 and len(self.detalles.get()) != 0


    def cua_limpiar(self):
        self.fecha
        self.detalles.delete(0, END)
        self.ingreso.delete(0, END)
        self.egreso.delete(0, END)

if __name__ == '__main__':
    root = Tk()
    programa = Gorventas(root)
    root.mainloop()
