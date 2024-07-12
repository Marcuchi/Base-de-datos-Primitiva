from flet import * 

def main(page:Page):
    def borrar_escrito(e):
        nombre.value = ""
        apellido.value = ""
        contraseña.value = ""
        page.update(page)
        
    def agregar_lista(e):
        #Si esta vacio el nombre del usuario
        if nombre.value == "":
            return
        else:
            base = open("./BaseDatos.txt", "a")
            texto = str(f"{nombre.value},{apellido.value},{contraseña.value}")
            base.write(texto+"\n")
            base.close()
            datos.append({"nombre": nombre.value,"Apellido": apellido.value,"Contraseña": contraseña.value})
            tabla.rows.append(DataRow(cells=[DataCell(Text(nombre.value)),DataCell(Text(apellido.value)),DataCell(Text(contraseña.value))]))
            borrar_escrito(e)
            page.update(tabla)
            
    def filtrar(e):
        filtrado = buscador.value.lower()
        myfiler = list(filter(lambda x: filtrado in x["nombre"].lower(),datos))
        tabla.rows = []
        #La tabla es solo visual, busco en mi diccionario
        if filtrado != "":
            if len(myfiler) > 0:
                for x in myfiler:
                    tabla.rows.append(
                        DataRow(cells=[
                        DataCell(Text(x['nombre'])),
                        DataCell(Text(x['Apellido'])),
                        DataCell(Text(x['Contraseña']))]
                                    )
                        )
                    page.update()
            else:
                page.update()
            
                
        else:
            for x in datos:
                tabla.rows.append(
                    DataRow(cells=[
                    DataCell(Text(x['nombre'])),
                    DataCell(Text(x['Apellido'])),
                    DataCell(Text(x['Contraseña']))]
                                 )
                     )
                page.update()

    def borrar_base(e):
        open("./BaseDatos.txt", "w").close()
        tabla.rows = []
        page.update()

    #Creo / reviso existencia de base de datos
    open("./BaseDatos.txt", "a").close()
    #Abro para escribir datos
    base = open("./BaseDatos.txt", "r")
    datos = []
    for x in base.readlines():
        nombre,apellido,contraseña = x.strip().split(',')
        datos.append({"nombre": nombre, "Apellido": apellido, "Contraseña": contraseña})
    base.close()


    # Inicializacion tabla
    tabla = DataTable(columns=[DataColumn(Text("Nombre")),
                                        DataColumn(Text("Apellido")),
                                        DataColumn(Text("Contraseña")) ],
                        rows=[]
                        )
    #Incorporo los datos de la lista a la tabla visual
    for x in datos:
        tabla.rows.append(
            DataRow(cells=[
                DataCell(Text(x['nombre'])),
                DataCell(Text(x['Apellido'])),
                DataCell(Text(x['Contraseña']))]
            )
        )


    #Configuracion Pagina    
    page.title = "Base de datos primitiva"
    page.window.width = 500
    page.window.height = 800
    page.window.resizable = False
    page.window.maximizable = False
    
    #Campos de Ingreso
    titulo = Text(value="Listado General", color="Blue",size=20,text_align=TextAlign.RIGHT)
    nombre = TextField(label="Nombre",color = "red",visible=True)
    apellido = TextField(label="Apellido", color = "red",visible=True)
    contraseña =  TextField(label="Contraseña", color = "Blue",password=True,can_reveal_password=True,visible=True)
    ingresar = ElevatedButton(text="Ingresar", color = "Red",on_click=agregar_lista)
    borrar = ElevatedButton(text="Borrar", color = "Red",on_click=borrar_escrito)
    buscador = SearchBar(bar_hint_text="Buscar...",bar_overlay_color="Red",on_change=filtrar,height=40,width=250)
    eliminar = ElevatedButton(text="Eliminar Base", color = "Red",on_click=borrar_base)


    contenedor_titulo =Container(content=titulo,alignment=alignment.center)
    contenedor_1 = Container(content=Column([nombre,apellido,contraseña],alignment=alignment.center),alignment=alignment.center)
    contenedor_2 = Container(content=Row([ingresar,borrar,buscador]),alignment=alignment.center)
    divisor = Divider(height=2, thickness=1)
    contenedor_3 = Container(content=tabla,alignment=alignment.center)
    contenedor_4 = Container(content=eliminar,alignment=alignment.center)
    

    page.add(contenedor_titulo,
             contenedor_1,
             contenedor_2,
             divisor,
             contenedor_3,
             contenedor_4)
    
app(main)