from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook

# Configurar el controlador de Firefox
firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = False  # Puedes cambiarlo a True si no quieres una ventana visible

# Crear una instancia del navegador Firefox
driver = webdriver.Firefox(options=firefox_options)

# Abrir la página web
driver.get("https://www.ejemplo.com")

# Crear una ruta para guardar los archivos
ruta_guardado = "C:/ruta/del/directorio/"  # Cambia esto a la ruta deseada

# Crear un libro de Excel y una hoja de trabajo
wb = Workbook()
ws = wb.active
ws.title = "Informacion_Web"

# Encabezados
ws.append(["Texto", "Enlace", "Fuente de la imagen"])

# Extraer información de la página
elements = driver.find_elements_by_css_selector("body *")  # Puedes ajustar el selector según la estructura de la página

for element in elements:
    text = element.text
    link = element.get_attribute("href")
    img_src = element.get_attribute("src")

    # Añadir información a la hoja de trabajo
    ws.append([text, link, img_src])

# Guardar el archivo Excel en la ruta especificada
archivo_excel = ruta_guardado + "informacion_web.xlsx"
wb.save(archivo_excel)

# Cerrar el navegador al finalizar
driver.quit()

print(f"Los datos han sido guardados en {archivo_excel}")
