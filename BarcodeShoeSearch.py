import cv2
from pyzbar.pyzbar import decode
import time
import requests
import pandas as pd

# Inicializa la cámara web
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Ancho
cap.set(4, 480)  # Alto

# Variables para el escáner de códigos de barras
codigos_detectados = set()
codigo_temporal = None
tiempo_deteccion = None
tiempo_para_estabilizar = 2.0
mensaje = ""
tiempo_mensaje_detectado = None

# Función para obtener información del producto a través de la API
def obtener_info_producto(upc):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
    }
    response = requests.get(f'https://api.upcitemdb.com/prod/trial/lookup?upc={upc}', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

try:
    while True:
        success, frame = cap.read()
        if success:
            for barcode in decode(frame):
                my_code = barcode.data.decode('utf-8')
                if my_code != codigo_temporal:
                    codigo_temporal = my_code
                    tiempo_deteccion = time.time()
                    mensaje = "Estabilizando..."

                if tiempo_deteccion and time.time() - tiempo_deteccion > tiempo_para_estabilizar:
                    if my_code not in codigos_detectados:
                        codigos_detectados.add(my_code)
                        mensaje = f"Codigo detectado: {my_code}"
                        tiempo_mensaje_detectado = time.time()
                    tiempo_deteccion = None

            if mensaje:
                if not tiempo_mensaje_detectado or time.time() - tiempo_mensaje_detectado < 3:
                    cv2.putText(frame, mensaje, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    mensaje = ""
                    tiempo_mensaje_detectado = None

            cv2.imshow('Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Finalizando escaneo.")
                break
finally:
    cap.release()
    cv2.destroyAllWindows()

# Procesar los códigos de barras detectados
products_info = []
for codigo in codigos_detectados:
    data = obtener_info_producto(codigo)
    if data and 'items' in data:
        for item in data['items']:
            product_dict = {
                'Código_barras': item.get('upc', 'No UPC'),
                'Producto': item.get('title', 'No Title'),
                'Marca': item.get('brand', 'No Brand'),
                'Modelo': item.get('model', 'No Model'),
                'Color': item.get('color', 'No Color'),
                'Talla': '',  # Se actualizará más adelante
                'Género': '',  # Se actualizará más adelante
                'Categoría': item.get('category', 'No Category'),
                'URL Imagen': item['images'][0] if item['images'] else 'No Image'
            }

            # Intentar extraer el tamaño y el género del título
            title = item.get('title', '')
            if "Women's" in title:
                product_dict['Género'] = "Women's"
            elif "Men's" in title:
                product_dict['Género'] = "Men's"

            # Extraer la talla si está especificada en el título
            size_split = title.split('Size')
            if len(size_split) > 1:
                product_dict['Talla'] = size_split[1].split()[0]

            # Añadir el diccionario a la lista
            products_info.append(product_dict)
    else:
        print(f"No se encontraron artículos para el código de barras {codigo}.")

# Crear un DataFrame de Pandas con la lista de productos
df_products = pd.DataFrame(products_info)

# Guardar el DataFrame en un archivo Excel
excel_path = 'products_info.xlsx'
df_products.to_excel(excel_path, index=False)

print(f"Archivo Excel guardado en {excel_path}")
