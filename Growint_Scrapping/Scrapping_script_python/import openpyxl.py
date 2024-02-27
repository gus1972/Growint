import openpyxl
from googletrans import Translator, LANGUAGES
from httpcore import ReadTimeout

def traducir_excel(ruta_origen, ruta_destino):
    # Cargar el libro de trabajo de Excel
    libro = openpyxl.load_workbook(ruta_origen)
    hoja = libro.active

    # Inicializar el traductor
    traductor = Translator(service_urls=['translate.google.com'])

    # Recorrer las celdas y traducir el texto
    for fila in hoja.iter_rows():
        for celda in fila:
            if celda.value:
                try:
                    # Traducir del chino al español
                    traduccion = traductor.translate(celda.value, src='zh-cn', dest='es')
                    celda.value = traduccion.text
                except ReadTimeout:
                    print("A ReadTimeout error occurred.")
                    # Here you can add code to retry the request or handle the error in another way

    # Guardar el libro de trabajo traducido
    libro.save(ruta_destino)

# Uso de la función
traducir_excel('C:/Users/Gusta/OneDrive/Documentos/ficheros_crowint/masqmai traffic 052023B.xlsx', 'C:/Users/Gusta/OneDrive/Documentos/ficheros_crowint/Tmasqmai traffic 052023B.xlsx')
