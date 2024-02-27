import openpyxl
from googletrans import Translator

def traducir_excel(ruta_origen, ruta_destino):
    # Cargar el libro de trabajo de Excel
    libro = openpyxl.load_workbook(ruta_origen)
    hoja = libro.active
    #print(libro)
    #print(hoja)

    # Inicializar el traductor
    traductor = Translator()

    # Recorrer las celdas y traducir el texto
    for fila in hoja.iter_rows():
        for celda in fila:
            if celda.value:
                # Traducir del chino al español
                traduccion = traductor.translate(celda.value, src='zh-cn', dest='es')
                #print(traduccion)
                celda.value = traduccion.text
                #print(celda.value)

    # Guardar el libro de trabajo traducido
    libro.save(ruta_destino)

# Uso de la función
traducir_excel('C:/Users/Gusta/Nextcloud/Marcas/TMALL/02 Traffic/masqmai traffic 052023B.xlsx', 'C:/Users/Gusta/Nextcloud/Marcas/TMALL/02 Traffic/Tmasqmai traffic 052023b.xlsx')