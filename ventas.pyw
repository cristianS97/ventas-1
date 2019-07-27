# -*- coding: utf-8 -*-
# Autor: Cristian Sáez Mardones
# Fecha: 19-07-2019
# Versión: 1.5.0
# Objetivo: Crear un sistema de gestión de productos y ventas

# Importación de archivo
    # Si hay
# Importación de bibliotecas
    # Si hay
# Importación de funciones
    # No hay

# Importación de bibliotecas
import tkinter as tk # Importamos tkinter para crear las interfaces graficas
from tkinter import messagebox # Importamos messagebox para poder crear ventanas emergentes
from tkinter import ttk # Importamos ttk para poder hacer uso de sus funciones
from tkinter import scrolledtext # Importamos scrolledtext para poder mostrar información en pantalla
import re # Importamos el módulo re para hacer uso de expresiones regulares
import sqlite3 # Importamos sqlite3 para crear y acceder a bases de datos
import os # Importamos las funciones del sistema operativo

# Importación de la ruta en donde se encuentra el archivo python
ruta = os.path.dirname(os.path.abspath(__file__))

###### FUNCIONES ######

# Función: Abrir la conexión con la base de datos
# Entrada: No hay entrada en la función
# Salida: No hay salida en la función
def abrirConexion():
    conexion = sqlite3.connect(f"{ruta}\\local.db")
    return conexion

# Función: Crear las tablas en la base de datos
# Entrada: No hay entrada en la función
# Salida: No hay salida en la función
def crearTablas():
    # Abrir la conexión
    conexion = abrirConexion()
    cursor = conexion.cursor()
    # Crear las tablas
    try:
        cursor.execute("""
            CREATE TABLE usuarios(
                id integer primary key AUTOINCREMENT,
                user varchar(20) unique,
                password varchar(50),
                rol varchar(20)
            )
        """)
        cursor.execute("""
            CREATE TABLE productos(
                id integer primary key AUTOINCREMENT,
                nombre varchar(30),
                marca varchar(20),
                precioCompra integer,
                precioVenta integer,
                pedidos integer,
                vendidos integer
            )
        """)
        cursor.execute("""
            CREATE TABLE descuentos(
                id integer primary key AUTOINCREMENT,
                producto varchar(30),
                descuento integer
            )
        """)
        cursor.execute("""
            CREATE TABLE pedidos(
                id integer primary key AUTOINCREMENT,
                producto varchar(30),
                cantidad integer,
                mensaje text
            )
        """)
        cursor.execute("""
            CREATE TABLE ganancias(
                id integer primary key AUTOINCREMENT,
                dia integer,
                mes integer,
                year integer,
                ganancias integer
            )
        """)
        print("Se crearon las tablas")
    except sqlite3.OperationalError:
        print("Las tablas ya existen en las bases de datos")
    finally:
        # Cerrar la conexión
        conexion.commit()
        conexion.close()

# Función: Insertar al superusuario en la base de datos
# Entrada: No hay entrada en la función
# Salida: No hay salida en la función
def insertarSuperUsuario():
    # Abrir la conexión
    conexion = abrirConexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("insert into usuarios (id, user, password, rol) values(null, 'admin', 'admin123', 'superusuario')")
        print("Superusuario ingresado correctamente")
    except sqlite3.IntegrityError:
        print("El superusuario admin ya existe")
    finally:
        # Cerrar la conexión
        conexion.commit()
        conexion.close()

# Función: Buscar un usuario en la base de datos
# Entrada: Nombre del usuario a buscar
# Salida: None si no encuentra al usuario, en caso contrario, retornara a este
def buscarUsuarios(usuario):
    conexion = abrirConexion()
    cursor = conexion.cursor()
    cursor.execute("select * from usuarios where user = ?", usuario)
    usuario = cursor.fetchone()
    conexion.close()
    return usuario

# Función: Insertar un usuario en la base de datos
# Entrada: Datos del usuario a insertar
# Salida: No hay salida en la función
def insertarUsuario(datos):
    # Abrimos la conexión
    conexion = abrirConexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("insert into usuarios(id, user, password, rol) values (null, ?, ?, ?)", datos)
        messagebox.showinfo(title="Registro exitoso", message="El registro se ha realizado con exito")
    except sqlite3.IntegrityError:
        messagebox.showerror(title="Usuario existente", message="El usuario ya existe en la base de datos")
    finally:
        # Cerramos la conexión
        conexion.commit()
        conexion.close()

###### Clase que crea la ventana de login ######
class Login:
    def __init__(self):
        crearTablas()
        insertarSuperUsuario()
        self.crearVentana()

    def crearVentana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Login de usuario")
        self.pedirDatos()
        self.crearBotones()
        self.ventana.mainloop()

    def pedirDatos(self):
        self.usuario = tk.StringVar()
        self.labelUsuario = tk.Label(self.ventana, text="Usuario")
        self.labelUsuario.grid(column=0, row=0, padx=10, pady=10)

        self.cajaUsuario = tk.Entry(self.ventana, textvariable=self.usuario)
        self.cajaUsuario.grid(column=1, row=0, padx=10, pady=10)

        self.password = tk.StringVar()
        self.labelPassword = tk.Label(self.ventana, text="Contraseña")
        self.labelPassword.grid(column=0, row=1, padx=10, pady=10)

        self.cajaPassword = tk.Entry(self.ventana, textvariable=self.password)
        self.cajaPassword.config(show="*")
        self.cajaPassword.grid(column=1, row=1, padx=10, pady=10)

    def crearBotones(self):
        self.botonRegistrar = tk.Button(self.ventana, text="Registrar", command=self.registrarUsuario)
        self.botonRegistrar.grid(column=0, row=2, padx=10, pady=10)

        self.botonIngresar = tk.Button(self.ventana, text="Ingresar", command=self.verificarUsuario)
        self.botonIngresar.grid(column=1, row=2, padx=10, pady=10)
    
    ############# FUNCIONES #############
    
    def verificarUsuario(self):
        self.usuarioBaseDeDatos = buscarUsuarios((self.usuario.get(),))
        if self.usuario.get() == "":
            messagebox.showwarning(title="Usuarios", message="Ingrese su Usuario")
        elif self.password.get() == "":
            messagebox.showwarning(title="Contraseña", message="Ingrese la contraseña")
        elif self.usuarioBaseDeDatos == None:
            messagebox.showwarning(title="Error", message="Los datos ingresados no estan correctos")
        elif self.usuario.get() != self.usuarioBaseDeDatos[1] or self.password.get() != self.usuarioBaseDeDatos[2]:
            messagebox.showwarning(title="Datos erroneos", message="Los datos ingresados no son correctos")
        else:
            messagebox.showinfo(title="Usuario", message="Datos correctos")
            self.ventana.destroy()
            self.ventanaVentas = Ventas(self.usuario.get(), self.password.get(), self.usuarioBaseDeDatos[3])
    
    def registrarUsuario(self):
        self.ventana.destroy()
        self.ventanaRegistro = Registro()

class Registro:
    def __init__(self):
        self.crearVentana()

    def crearVentana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Registro")
        self.pedirDatos()
        self.crearBotones()
        self.ventana.mainloop()

    def pedirDatos(self):
        self.frameRegistro = tk.Frame(self.ventana)
        self.frameRegistro.pack()
        self.frameConfirmar = tk.Frame(self.ventana)
        self.frameConfirmar.pack()

        self.labelRegistro = tk.Label(self.frameRegistro, text="Datos Registro")
        self.labelRegistro.grid(column=0, row=0, padx=10, pady=10)

        self.usuario = tk.StringVar()
        self.labelUsuario = tk.Label(self.frameRegistro, text="Usuario")
        self.labelUsuario.grid(column=0, row=1, padx=10, pady=10)

        self.cajaUsuario = tk.Entry(self.frameRegistro, textvariable=self.usuario)
        self.cajaUsuario.grid(column=1, row=1, padx=10, pady=10)

        self.password = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegistro, text="Contraseña")
        self.labelPassword.grid(column=0, row=2, padx=10, pady=10)

        self.cajaPassword = tk.Entry(self.frameRegistro, textvariable=self.password)
        self.cajaPassword.config(show="*")
        self.cajaPassword.grid(column=1, row=2, padx=10, pady=10)

        self.password2 = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegistro, text="Verifica contraseña")
        self.labelPassword.grid(column=0, row=3, padx=10, pady=10)

        self.cajaPassword = tk.Entry(self.frameRegistro, textvariable=self.password2)
        self.cajaPassword.config(show="*")
        self.cajaPassword.grid(column=1, row=3, padx=10, pady=10)

        self.rol = tk.StringVar()
        self.labelRol = tk.Label(self.frameRegistro, text="Seleccione un rol")
        self.labelRol.grid(column=0, row=4, padx=10, pady=10)

        self.roles = ("vendedor", "superusuario")
        self.spinboxRol = tk.Spinbox(self.frameRegistro, values=self.roles, textvariable=self.rol)
        self.spinboxRol.grid(column=1, row=4, padx=10, pady=10)

        self.labelSuperUsuario = tk.Label(self.frameConfirmar, text="Datos super usuario")
        self.labelSuperUsuario.grid(column=0, row=0, padx=10, pady=10)

        self.admin = tk.StringVar()
        self.labelAdmin = tk.Label(self.frameConfirmar, text="Super usuario")
        self.labelAdmin.grid(column=0, row=1, padx=10, pady=10)

        self.cajaAdmin = tk.Entry(self.frameConfirmar, textvariable=self.admin)
        self.cajaAdmin.grid(column=1, row=1, padx=10, pady=10)

        self.passwordAdmin = tk.StringVar()
        self.labelPasswordAdmin = tk.Label(self.frameConfirmar, text="Contraseña")
        self.labelPasswordAdmin.grid(column=0, row=2, padx=10, pady=10)

        self.cajaPasswordAdmin = tk.Entry(self.frameConfirmar, textvariable=self.passwordAdmin)
        self.cajaPasswordAdmin.config(show="*")
        self.cajaPasswordAdmin.grid(column=1, row=2, padx=10, pady=10)
        
    def crearBotones(self):
        self.botonRegistrar = tk.Button(self.frameConfirmar, text="Registrar", command=self.registrarUsuario)
        self.botonRegistrar.grid(column=0, row=3, padx=10, pady=10)

        self.botonIngresar = tk.Button(self.frameConfirmar, text="Ingresar", command=self.ingresar)
        self.botonIngresar.grid(column=1, row=3, padx=10, pady=10)
    
    ############# FUNCIONES #############

    def ingresar(self):
        self.ventana.destroy()
        self.ventanaLogin = Login()
    
    def registrarUsuario(self):
        self.datos = (self.usuario.get(), self.password.get(), self.rol.get())
        self.usuarioBaseDeDatos = buscarUsuarios((self.admin.get(),))
        if self.usuario.get() == "":
            messagebox.showwarning(title="Usuario", message="Ingrese un usuario")
        elif self.password.get() == "" or self.password2.get() == "":
            messagebox.showwarning(title="Contraseñas", message="Rellene ambas contraseñas")
        elif self.password.get() != self.password2.get():
            messagebox.showerror(title="Error en la contraseña", message="Las contraseñas son distintas")
        elif len(self.password.get()) < 8:
            messagebox.showwarning(title="Largo de contraseña", message="La contraseña debe tener al menos 8 caracteres")
        elif re.search('[0-9]', self.password.get()) is None:
            messagebox.showwarning(title="Contraseña", message="Su contraseña debe poseer al menos un número")
        elif re.search('[a-z]', self.password.get()) is None: 
            messagebox.showwarning(title="Contraseña", message="Su contraseña debe poseer minusculas")
        elif re.search('[A-Z]', self.password.get()) is None: 
            messagebox.showwarning(title="Contraseña", message="Su contraseña debe poseer mayusculas")
        elif self.admin.get() == "" or self.passwordAdmin.get() == "":
            messagebox.showwarning(title="Super usuario", message="Los datos del super usuario son necesarios para confirmar")
        elif self.admin.get() != self.usuarioBaseDeDatos[1] or self.passwordAdmin.get() != self.usuarioBaseDeDatos[2] or self.usuarioBaseDeDatos == None or self.usuarioBaseDeDatos[3] != "superusuario":
            messagebox.showwarning(title="Super usuario", message="Los datos del super usuario son incorrectos")
        else:
            insertarUsuario(self.datos)
            self.ingresar()

class Ventas:
    def __init__(self, usuario, password, estado):
        self.conexion = (usuario, password, estado)
        self.crearVentana()

    def crearVentana(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ventas local")
        self.crearCuaderno()
        self.crearSalida()
        self.ventana.mainloop()
    
    def crearCuaderno(self):
        self.secciones = ttk.Notebook(self.ventana)
        self.seccionListado()
        self.seccionVenta()
        if self.conexion[2] == "superusuario":
            self.seccionPedido()
            self.seccionRegistro()
            self.seccionPendientes()
            self.seccionGanancias()
            self.seccionModificaciones()
        self.secciones.grid(column=0, row=0, padx=10, pady=10)
    
    def crearSalida(self):
        self.botonSalir = tk.Button(self.ventana, text = "Salir", command = self.salida)
        self.botonSalir.grid(column = 0, row = 1, padx = 10, pady = 10)

    def seccionListado(self):
        self.pagina1 = ttk.Frame(self.secciones)
        self.frameProductos = tk.Frame(self.pagina1)
        self.frameBuscar = tk.Frame(self.pagina1)
        self.frameBotones = tk.Frame(self.pagina1)
        self.frameProductos.pack()
        self.frameBuscar.pack()
        self.frameBotones.pack()
        self.secciones.add(self.pagina1, text="Stock de productos")
        self.labelFrame1 = ttk.LabelFrame(self.frameProductos, text = "Productos")
        self.labelFrame1.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.listaProductos = scrolledtext.ScrolledText(self.frameProductos, width=50, height=30)
        self.listaProductos.grid(column=0, row=1, padx=10, pady=10)

        self.labelNombre = tk.Label(self.frameBuscar, text="Nombre producto:")
        self.labelNombre.grid(row=0, column=0, padx=10, pady=10)
        self.nombreProducto = tk.StringVar()
        self.cuadroNombreProducto = tk.Entry(self.frameBuscar, textvariable=self.nombreProducto)
        self.cuadroNombreProducto.grid(row=0, column=1, padx=10, pady=10)
        self.botonBuscarProducto = tk.Button(self.frameBuscar, text="Buscar")
        self.botonBuscarProducto.grid(row=0, column=2, padx=10, pady=10)

        self.botonBuscar = tk.Button(self.frameBotones, text="Listar productos")
        self.botonBuscar.grid(column=0, row=0, padx=10, pady=10)
        self.botonLimpiar = tk.Button(self.frameBotones, text="Limpiar productos")
        self.botonLimpiar.grid(column=1, row=0, padx=10, pady=10)
    
    def seccionVenta(self):
        self.productosVendidos = list()
        self.pagina2 = ttk.Frame(self.secciones)

        self.frameVentas()
        self.buscarProducto()
        self.datosBoleta()

        self.secciones.add(self.pagina2, text="Venta local")
    
    def frameVentas(self):
        self.frameDatos = tk.Frame(self.pagina2)
        self.frameProductos = tk.Frame(self.pagina2)
        self.frameBotoneProductos = tk.Frame(self.pagina2)
        self.frameBoleta = tk.Frame(self.pagina2)
        self.frameBotonesBoleta = tk.Frame(self.pagina2)

        self.frameDatos.pack()
        self.frameProductos.pack()
        self.frameBotoneProductos.pack()
        self.frameBoleta.pack()
        self.frameBotonesBoleta.pack()
    
    def buscarProducto(self):
        self.labelNombreProducto = tk.Label(self.frameDatos, text = "Nombre producto: ")
        self.labelNombreProducto.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.producto = tk.StringVar()
        self.cajaBusquedaProducto = tk.Entry(self.frameDatos, textvariable = self.producto)
        self.cajaBusquedaProducto.grid(column = 1, row = 0, padx = 10, pady = 10)
        self.botonBuscar = tk.Button(self.frameDatos, text="Buscar")
        self.botonBuscar.grid(column = 2, row = 0, padx = 10, pady = 10)

        self.listaProductos = scrolledtext.ScrolledText(self.frameProductos, width=50, height=8)
        self.listaProductos.grid(column=0, row=0, padx=10, pady=10)

        self.id = tk.IntVar()
        self.labelId = tk.Label(self.frameBotoneProductos, text = "ID del producto")
        self.labelId.grid(column=0, row=0, padx=10, pady=10)
        self.idSeleccionar = tk.Entry(self.frameBotoneProductos, textvariable = self.id)
        self.idSeleccionar.grid(column=1, row=0, padx=10, pady=10)
        self.botonAgregar = tk.Button(self.frameBotoneProductos, text = "Agregar a la boleta")
        self.botonAgregar.grid(column=2, row=0, padx=10, pady=10)
        self.botonBorrar = tk.Button(self.frameBotoneProductos, text = "Borrar de la boleta")
        self.botonBorrar.grid(column=3, row=0, padx=10, pady=10)
    
    def datosBoleta(self):
        self.labelBoleta = tk.Label(self.frameBoleta, text = "Datos de la boleta")
        self.labelBoleta.grid(column=0, row=0, padx=10, pady=10)
        self.listaProductos = scrolledtext.ScrolledText(self.frameBoleta, width=50, height=12)
        self.listaProductos.grid(column=0, row=1, padx=10, pady=10)

        self.botonDescartar = tk.Button(self.frameBotonesBoleta, text = "Descartar boleta")
        self.botonDescartar.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.labelMetodoPago = tk.Label(self.frameBotonesBoleta, text = "Seleccione método de pago: ")
        self.labelMetodoPago.grid(column = 1, row = 0, padx = 10, pady = 10)
        self.mediosDePago = ("Efectivo", "Tarjeta crédito", "Tarjeta débito", "Transferencia")
        self.pago = tk.StringVar()
        self.spinboxRol = tk.Spinbox(self.frameBotonesBoleta, values=self.mediosDePago, textvariable = self.pago)
        self.spinboxRol.grid(column = 2, row = 0, padx = 10, pady = 10)
        
        self.labelEfectivo = tk.Label(self.frameBotonesBoleta, text ="Efectivo: ")
        self.labelEfectivo.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.monto = tk.IntVar()
        self.cajaMonto = tk.Entry(self.frameBotonesBoleta, textvariable = self.monto)
        self.cajaMonto.grid(column = 1, row = 1, padx = 10, pady = 10)
        self.botonPagar = tk.Button(self.frameBotonesBoleta, text = "Pagar")
        self.botonPagar.grid(column = 2, row = 1, padx = 10, pady = 10)
    
    def seccionPedido(self):
        self.pagina3 = ttk.Frame(self.secciones)
        
        self.crearFramesPedido()
        self.datosProductos()
        self.cantidadPedidoFrame()
        self.resumenPedido()

        self.secciones.add(self.pagina3, text="Pedido proveedores")
    
    def crearFramesPedido(self):
        self.frameDatosPedidos = tk.Frame(self.pagina3)
        self.frameResumen = tk.Frame(self.pagina3)

        self.frameDatosPedidos.pack()
        self.frameResumen.pack()

        self.frameDatos = tk.Frame(self.frameDatosPedidos)
        self.framePedidos = tk.Frame(self.frameDatosPedidos)

        self.frameDatos.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.framePedidos.grid(row = 0, column = 1, padx = 10, pady = 10)
        
        self.framePedido = tk.Frame(self.framePedidos)
        self.frameMensaje = tk.Frame(self.framePedidos)
        
        self.framePedido.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.frameMensaje.grid(row = 1, column = 0, padx = 10, pady = 10)
    
    def datosProductos(self):
        self.labelID = tk.Label(self.frameDatos, text = "ID: ")
        self.labelID.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.id = tk.IntVar()
        self.cajaId = tk.Entry(self.frameDatos, textvariable = self.id)
        self.cajaId.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelNombre = tk.Label(self.frameDatos, text = "Nombre: ")
        self.labelNombre.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.nombre = tk.StringVar()
        self.cajaNombre = tk.Entry(self.frameDatos, textvariable = self.nombre)
        self.cajaNombre.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.labelMarca = tk.Label(self.frameDatos, text = "Marca: ")
        self.labelMarca.grid(column = 0, row = 2, padx = 10, pady = 10)
        self.marca = tk.StringVar()
        self.cajaMarca = tk.Entry(self.frameDatos, textvariable = self.marca, state = "readonly")
        self.cajaMarca.grid(column = 1, row = 2, padx = 10, pady = 10)

        self.labelCompra = tk.Label(self.frameDatos, text = "Precio compra: ")
        self.labelCompra.grid(column = 0, row = 3, padx = 10, pady = 10)
        self.precioCompra = tk.StringVar()
        self.cajaCompra = tk.Entry(self.frameDatos, textvariable = self.precioCompra, state = "readonly")
        self.cajaCompra.grid(column = 1, row = 3, padx = 10, pady = 10)

        self.labelVenta = tk.Label(self.frameDatos, text = "Precio Venta: ")
        self.labelVenta.grid(column = 0, row = 4, padx = 10, pady = 10)
        self.precioVenta = tk.StringVar()
        self.cajaVenta = tk.Entry(self.frameDatos, textvariable = self.precioVenta, state = "readonly")
        self.cajaVenta.grid(column = 1, row = 4, padx = 10, pady = 10)

        self.labelPedidos = tk.Label(self.frameDatos, text = "Pedidos: ")
        self.labelPedidos.grid(column = 0, row = 5, padx = 10, pady = 10)
        self.pedido = tk.IntVar()
        self.cajaPedido = tk.Entry(self.frameDatos, textvariable = self.pedido, state = "readonly")
        self.cajaPedido.grid(column = 1, row = 5, padx = 10, pady = 10)

        self.labelVendidos = tk.Label(self.frameDatos, text = "Vendidos: ")
        self.labelVendidos.grid(column = 0, row = 6, padx = 10, pady = 10)
        self.pedido = tk.IntVar()
        self.cajaPedido = tk.Entry(self.frameDatos, textvariable = self.pedido, state = "readonly")
        self.cajaPedido.grid(column = 1, row = 6, padx = 10, pady = 10)

        self.botonBorrar = tk.Button(self.frameDatos, text = "Limpiar campos")
        self.botonBorrar.grid(column = 0, row = 7, padx = 10, pady = 10)
        self.botonBuscar = tk.Button(self.frameDatos, text = "Buscar producto")
        self.botonBuscar.grid(column = 1, row = 7, padx = 10, pady = 10)

    def cantidadPedidoFrame(self):
        self.labelPedido = tk.Label(self.framePedido, text = "Cantidad a pedir: ")
        self.labelPedido.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.cantidadPedido = tk.IntVar()
        self.cajaPedido = tk.Entry(self.framePedido, textvariable = self.cantidadPedido)
        self.cajaPedido.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelMensaje = tk.Label(self.frameMensaje, text = "Mensaje:")
        self.labelMensaje.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.scrollMensaje = scrolledtext.ScrolledText(self.frameMensaje, width = 25, height = 10)
        self.scrollMensaje.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.botonAgregar = tk.Button(self.frameMensaje, text = "Añadir")
        self.botonAgregar.grid(column = 0, row = 2, padx = 10, pady = 10)
    
    def resumenPedido(self):
        self.labelResumen = tk.Label(self.frameResumen, text = "Resumen del pedido")
        self.labelResumen.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.scrollResumen = scrolledtext.ScrolledText(self.frameResumen, width = 50, height = 10)
        self.scrollResumen.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.botonPedir = tk.Button(self.frameResumen, text = "Realizar pedido")
        self.botonPedir.grid(column = 0, row = 2, padx = 10, pady = 10)
    
    def seccionRegistro(self):
        self.pagina4 = tk.Frame(self.secciones)

        self.crearFramesRegistro()
        self.pedirDatosUsuario()
        self.pedirDatosSuperusuario()        

        self.secciones.add(self.pagina4, tex ="Registro de usuarios")

    def crearFramesRegistro(self):
        self.frameRegistrados = tk.Frame(self.pagina4)
        self.frameModificar = tk.Frame(self.pagina4)
        self.frameRegistrar = tk.Frame(self.pagina4)

        self.frameRegistrados.pack()
        self.frameModificar.pack()
        self.frameRegistrar.pack()
    
    def pedirDatosUsuario(self):
        self.labelRegistros = tk.Label(self.frameRegistrados, text = "Usuarios registrados en la base de datos")
        self.labelRegistros.grid(column = 0, row = 0, padx = 10, pady = 10)
        self.scrollResumen = scrolledtext.ScrolledText(self.frameRegistrados, width = 60, height = 10)
        self.scrollResumen.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.labelModificaciones = tk.Label(self.frameModificar, text = "Datos para modificar")
        self.labelModificaciones.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.labelId = tk.Label(self.frameModificar, text = "Id:")
        self.labelId.grid(column = 0, row = 1, padx = 10, pady = 10)
        self.id = tk.IntVar()
        self.cuadroId = tk.Entry(self.frameModificar, textvariable = self.id)
        self.cuadroId.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.labelNombre = tk.Label(self.frameModificar, text = "Usuario:")
        self.labelNombre.grid(column = 2, row = 1, padx = 10, pady = 10)
        self.nombre = tk.StringVar()
        self.cuadroNombre = tk.Entry(self.frameModificar, textvariable = self.nombre)
        self.cuadroNombre.grid(column = 3, row = 1, padx = 10, pady = 10)

        self.labelRol = tk.Label(self.frameModificar, text = "Rol:")
        self.labelRol.grid(column = 0, row = 2, padx = 10, pady = 10)
        self.roles = ("vendedor", "superusuario")
        self.rol = tk.StringVar()
        self.spinboxRol = tk.Spinbox(self.frameModificar, values=self.roles, textvariable=self.rol)
        self.spinboxRol.grid(column = 1, row = 2, padx = 10, pady = 10)

        self.labelPassword = tk.Label(self.frameModificar, text = "Contraseña:")
        self.labelPassword.grid(column = 2, row = 2, padx = 10, pady = 10)
        self.password = tk.StringVar()
        self.cuadroPassword = tk.Entry(self.frameModificar, textvariable = self.password)
        self.cuadroPassword.grid(column = 3, row = 2, padx = 10, pady = 10)
    
    def pedirDatosSuperusuario(self):
        self.labelRegistro = tk.Label(self.frameRegistrar, text="Datos Registro")
        self.labelRegistro.grid(column=0, row=0, padx=10, pady=10)

        self.usuario = tk.StringVar()
        self.labelUsuario = tk.Label(self.frameRegistrar, text="Usuario")
        self.labelUsuario.grid(column=0, row=1, padx=10, pady=10)

        self.cajaUsuario = tk.Entry(self.frameRegistrar, textvariable=self.usuario)
        self.cajaUsuario.grid(column=1, row=1, padx=10, pady=10)

        self.password = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegistrar, text="Contraseña")
        self.labelPassword.grid(column=0, row=2, padx=10, pady=10)

        self.cajaPassword = tk.Entry(self.frameRegistrar, textvariable=self.password)
        self.cajaPassword.config(show="*")
        self.cajaPassword.grid(column=1, row=2, padx=10, pady=10)

        self.password2 = tk.StringVar()
        self.labelPassword = tk.Label(self.frameRegistrar, text="Verifica contraseña")
        self.labelPassword.grid(column=0, row=3, padx=10, pady=10)

        self.cajaPassword = tk.Entry(self.frameRegistrar, textvariable=self.password2)
        self.cajaPassword.config(show="*")
        self.cajaPassword.grid(column=1, row=3, padx=10, pady=10)

        self.rol = tk.StringVar()
        self.labelRol = tk.Label(self.frameRegistrar, text="Seleccione un rol")
        self.labelRol.grid(column=0, row=4, padx=10, pady=10)

        self.roles = ("vendedor", "superusuario")
        self.spinboxRol = tk.Spinbox(self.frameRegistrar, values=self.roles, textvariable=self.rol)
        self.spinboxRol.grid(column=1, row=4, padx=10, pady=10)

        # Datos super usuario
        self.labelSuperUsuario = tk.Label(self.frameRegistrar, text="Datos super usuario")
        self.labelSuperUsuario.grid(column=2, row=0, padx=10, pady=10)

        self.admin = tk.StringVar()
        self.labelAdmin = tk.Label(self.frameRegistrar, text="Super usuario")
        self.labelAdmin.grid(column=2, row=1, padx=10, pady=10)

        self.cajaAdmin = tk.Entry(self.frameRegistrar, textvariable=self.admin)
        self.cajaAdmin.grid(column=3, row=1, padx=10, pady=10)

        self.passwordAdmin = tk.StringVar()
        self.labelPasswordAdmin = tk.Label(self.frameRegistrar, text="Contraseña")
        self.labelPasswordAdmin.grid(column=2, row=2, padx=10, pady=10)

        self.cajaPasswordAdmin = tk.Entry(self.frameRegistrar, textvariable=self.passwordAdmin)
        self.cajaPasswordAdmin.config(show="*")
        self.cajaPasswordAdmin.grid(column=3, row=2, padx=10, pady=10)

        self.opcion = tk.StringVar()
        self.opcionRM = ("Registrar", "Modificar", "Eliminar")
        self.spinboxRol = tk.Spinbox(self.frameRegistrar, values=self.opcionRM, textvariable=self.opcion)
        self.spinboxRol.grid(column=2, row=3, padx=10, pady=10)

        self.botonConfirmar = tk.Button(self.frameRegistrar, text = "Confirmar")
        self.botonConfirmar.grid(column = 3, row = 3, padx = 10, pady = 10)
    
    def seccionPendientes(self):
        self.pagina5 = ttk.Frame(self.secciones)

        self.crearFramesPendientes()
        self.listaDePendientes()
        self.accionesPendientes()

        self.secciones.add(self.pagina5, tex ="Pedidos pendientes")
    
    def crearFramesPendientes(self):
        self.frameListaPendientes = tk.Frame(self.pagina5)
        self.frameAccionesPendientes = tk.Frame(self.pagina5)

        self.frameListaPendientes.pack()
        self.frameAccionesPendientes.pack()

    def listaDePendientes(self):
        self.scrollResumen = scrolledtext.ScrolledText(self.frameListaPendientes, width = 60, height = 30)
        self.scrollResumen.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.botonObtener = tk.Button(self.frameListaPendientes, text = "Obtener lista pendientes")
        self.botonObtener.grid(column = 0, row = 1, padx = 10, pady = 10)

    def accionesPendientes(self):
        self.labelId = tk.Label(self.frameAccionesPendientes, text = "Id producto:")
        self.labelId.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.id = tk.IntVar()
        self.cajaId = tk.Entry(self.frameAccionesPendientes, textvariable = self.id)
        self.cajaId.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.botonRealizado = tk.Button(self.frameAccionesPendientes, text = "Marcar como recibido")
        self.botonRealizado.grid(column = 2, row = 0, padx = 10, pady = 10)

        self.botonCancelar = tk.Button(self.frameAccionesPendientes, text = "Cancelar pedido")
        self.botonCancelar.grid(column = 3, row = 0, padx = 10, pady = 10)
    
    def seccionGanancias(self):
        self.pagina6 = ttk.Frame(self.secciones)

        self.crearFramesGanancias()
        self.listaGanacias()
        self.botonesGanancias()
        self.filtarFecha()

        self.secciones.add(self.pagina6, tex ="Ganancias")

    def crearFramesGanancias(self):
        self.frameGanancias = tk.Frame(self.pagina6)
        self.frameBotonesGanancias = tk.Frame(self.pagina6)
        self.frameFiltrarGanancias = tk.Frame(self.pagina6)

        self.frameGanancias.pack()
        self.frameBotonesGanancias.pack()
        self.frameFiltrarGanancias.pack()

    def listaGanacias(self):
        self.scrollResumen = scrolledtext.ScrolledText(self.frameGanancias, width = 60, height = 25)
        self.scrollResumen.grid(column = 0, row = 0, padx = 10, pady = 10)

    def botonesGanancias(self):
        self.botonObtener = tk.Button(self.frameBotonesGanancias, text = "Obtener lista de ganancias diarias")
        self.botonObtener.grid(column = 0, row = 0, padx = 10, pady = 10)
        
        self.botonLimpiar = tk.Button(self.frameBotonesGanancias, text = "Limpiar lista")
        self.botonLimpiar.grid(column = 1, row = 0, padx = 10, pady = 10)
    
    def filtarFecha(self):
        self.labelFecha = tk.Label(self.frameFiltrarGanancias, text = "Fecha a buscar")
        self.labelFecha.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.fechaBuscada = tk.StringVar()
        self.cuadroFecha = tk.Entry(self.frameFiltrarGanancias, textvariable = self.fechaBuscada)
        self.cuadroFecha.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.botonFiltrar = tk.Button(self.frameFiltrarGanancias, text = "Buscar")
        self.botonFiltrar.grid(column = 2, row = 0, padx = 10, pady = 10)

        self.labelMes = tk.Label(self.frameFiltrarGanancias, text = "Mes a buscar")
        self.labelMes.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.mesBuscado = tk.StringVar()
        self.cuadroMes = tk.Entry(self.frameFiltrarGanancias, textvariable = self.mesBuscado)
        self.cuadroMes.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.botonMes = tk.Button(self.frameFiltrarGanancias, text = "Buscar")
        self.botonMes.grid(column = 2, row = 1, padx = 10, pady = 10)
    
    def seccionModificaciones(self):
        self.pagina7 = ttk.Frame(self.secciones)

        self.crearFramesModificaciones()
        self.datosProducto()
        self.datosSuperUsuario()

        self.secciones.add(self.pagina7, tex ="Modificaciones")

    def crearFramesModificaciones(self):
        self.frameDatosProducto = tk.Frame(self.pagina7)
        self.frameDatosConfirmacion = tk.Frame(self.pagina7)

        self.frameDatosProducto.pack()
        self.frameDatosConfirmacion.pack()
    
    def datosProducto(self):
        self.labelId = tk.Label(self.frameDatosProducto, text = "Id:")
        self.labelId.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.idModificar = tk.IntVar()
        self.cuadroId = tk.Entry(self.frameDatosProducto, textvariable = self.idModificar)
        self.cuadroId.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelNombre = tk.Label(self.frameDatosProducto, text = "Nombre:")
        self.labelNombre.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.nombreModificar = tk.StringVar()
        self.cuadroNombre = tk.Entry(self.frameDatosProducto, textvariable = self.nombreModificar)
        self.cuadroNombre.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.labelMarca = tk.Label(self.frameDatosProducto, text = "Marca:")
        self.labelMarca.grid(column = 0, row = 2, padx = 10, pady = 10)

        self.marcaModificar = tk.StringVar()
        self.cuadroMarca = tk.Entry(self.frameDatosProducto, textvariable = self.marcaModificar)
        self.cuadroMarca.grid(column = 1, row = 2, padx = 10, pady = 10)

        self.labelCompra = tk.Label(self.frameDatosProducto, text = "Precio compra:")
        self.labelCompra.grid(column = 0, row = 3, padx = 10, pady = 10)

        self.compraModificar = tk.IntVar()
        self.cuadroCompra = tk.Entry(self.frameDatosProducto, textvariable = self.compraModificar)
        self.cuadroCompra.grid(column = 1, row = 3, padx = 10, pady = 10)

        self.labelVenta = tk.Label(self.frameDatosProducto, text = "Precio venta:")
        self.labelVenta.grid(column = 0, row = 4, padx = 10, pady = 10)

        self.ventaModificar = tk.IntVar()
        self.cuadroVenta = tk.Entry(self.frameDatosProducto, textvariable = self.ventaModificar)
        self.cuadroVenta.grid(column = 1, row = 4, padx = 10, pady = 10)

        self.labelDescuento = tk.Label(self.frameDatosProducto, text = "Descuento:")
        self.labelDescuento.grid(column = 0, row = 5, padx = 10, pady = 10)

        self.descuentoModificar = tk.IntVar()
        self.cuadroDescuento = tk.Entry(self.frameDatosProducto, textvariable = self.descuentoModificar)
        self.cuadroDescuento.grid(column = 1, row = 5, padx = 10, pady = 10)

        self.botonLimpiar = tk.Button(self.frameDatosProducto, text = "Limpiar datos")
        self.botonLimpiar.grid(column = 0, row = 6, padx = 10, pady = 10)

        self.botonBuscar = tk.Button(self.frameDatosProducto, text = "Buscar producto")
        self.botonBuscar.grid(column = 1, row = 6, padx = 10, pady = 10)
    
    def datosSuperUsuario(self):
        self.labelSuperUsuario = tk.Label(self.frameDatosConfirmacion, text = "Super usuario:")
        self.labelSuperUsuario.grid(column = 0, row = 0, padx = 10, pady = 10)

        self.superusuario = tk.StringVar()
        self.cajaSuperUsuario = tk.Entry(self.frameDatosConfirmacion, textvariable = self.superusuario)
        self.cajaSuperUsuario.grid(column = 1, row = 0, padx = 10, pady = 10)

        self.labelPassword = tk.Label(self.frameDatosConfirmacion, text = "Contraseña:")
        self.labelPassword.grid(column = 0, row = 1, padx = 10, pady = 10)

        self.password = tk.StringVar()
        self.cajaPassword = tk.Entry(self.frameDatosConfirmacion, textvariable = self.password)
        self.cajaPassword.config(show = "*")
        self.cajaPassword.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.botonConfirmarCambios = tk.Button(self.frameDatosConfirmacion, text = "Confirmar cambios")
        self.botonConfirmarCambios.grid(column = 1, row = 2, padx = 10, pady = 10)

    ############# FUNCIONES #############
    
    def salida(self):
        resp = messagebox.askyesno(title = "Seguro que desea salir?", message = "Esta seguro?")
        if resp:
            self.ventana.destroy()
        

########################
### Bloque principal ###
########################

objVentana = Login()