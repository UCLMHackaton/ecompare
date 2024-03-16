import requests
import pymongo
import json

flag = True

# Conexión a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ingestaMercadona"]
categories_collection = db["categorias-productos"]

# URL base de la API de Mercadona
base_url_categoria = "https://tienda.mercadona.es/api/categories/{}"
base_url_producto = "https://tienda.mercadona.es/api/products/{}"
base_url_detalle_producto = "https://world.openfoodfacts.org/api/v2/product/{}"

def guardar_producto_en_mongo(producto):
    # Comprobar si la categoría ya existe en MongoDB
    existing_category = categories_collection.find_one({"id": producto["id"]})
    if existing_category:
        print(f"El producto {producto['slug']} ya existe en la base de datos.")
    else:
        # Insertar la categoría en MongoDB
        categories_collection.insert_one(producto)
        print(f"Producto {producto['slug']} insertada en la base de datos.")
        
def obtener_productos_categoria(categoria):
        
    for c in categoria["categories"]:
        for producto in c["products"]:
            url = base_url_producto.format(producto["id"])
            response = requests.get(url)
            if response.status_code == 200:
                
                producto = response.json()
                url = base_url_detalle_producto.format(producto["ean"])
                response = requests.get(url)
                
                if response.status_code == 200:
                    detalle_producto = response.json()
                    producto["detalle"] = detalle_producto
                    guardar_producto_en_mongo(producto)
            else:
               ...
                

def obtener_categoria(categoria_id):
    url = base_url_categoria.format(categoria_id)
    flag = True
    response = requests.get(url)
    if response.status_code == 200:
        categoria = response.json()
        
        obtener_productos_categoria(categoria)

        if "children" in categoria:
            for child_id in categoria["children"]:
                obtener_categoria(child_id)
    else:
        flag = False
        print(f"No se pudo obtener la producto {categoria_id}")

    return flag
# Empezar con la categoría raíz
category_id = 1
while flag:
    obtener_categoria(category_id)
    category_id += 1
    
