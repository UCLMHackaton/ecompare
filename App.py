from flask import Flask, render_template
from flask_mysqldb import MySQL as mysql
from bs4 import BeautifulSoup
from pymongo import MongoClient as mc

app = Flask(__name__)

# Configurar Flask para manejar rutas sin la extensión .html
app.url_map.strict_slashes = False

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'paulino'
app.config['MYSQL_PASSWORD'] = 'zB3jDuB4imUQHcoRm6hgYKgLDkP'
app.config['MYSQL_DB'] = 'catalog_h4g'

conexion = mysql(app)

client = mc('mongodb://localhost:27017/')  # Conecta a la base de datos MongoDB
db = client['tu_basedatos']  # Selecciona tu base de datos
collection = db['tu_coleccion']


@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/contact')    
def Contact():
    return render_template('contact.html')

@app.route('/catalog')

def Catalog():
    return render_template('catalog.html', data = )

if __name__ == '__main__':    
    app.run(port = 3000, debug=True)
