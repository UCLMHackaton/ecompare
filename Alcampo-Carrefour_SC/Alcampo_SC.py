from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from unidecode import unidecode
import Utils
import time


def scrape_alcampo():
    # Configurar el controlador de Selenium (ChromeDriver)
    service = Service('chromedriver.exe', port=9516)
    options = Options()
    options.add_argument("--disable-notifications")  # Desactivar las notificaciones
    options.add_argument("--disable-popup-blocking")  # Desactivar el bloqueo de ventanas emergentes
    options.add_argument("--disable-infobars")  # Desactivar las barras de información
    options.add_argument("--accept_insecure_certs=true")  # Aceptar certificados no seguros
    options.add_argument("--start-maximized")  # Maximizar la ventana del navegador al inicio

    driver = webdriver.Chrome(service=service, options=options)
    url = 'https://www.compraonline.alcampo.es/categories?source=navigation'
    driver.get(url)

    # Definimos el número máximo de desplazamientos
    max_scrolls = 80
    products = []

    # Desplazamos la página hacia abajo en incrementos más pequeños
    for _ in range(max_scrolls):
        # Obtenemos la posición actual de la página antes del desplazamiento
        old_position = driver.execute_script("return window.pageYOffset;")

        # Desplazamos hacia abajo
        driver.execute_script("window.scrollBy(0, 1000);")

        # Esperamos un breve momento para que se carguen los elementos
        time.sleep(0.2)

        # Obtenemos la posición de la página después del desplazamiento
        new_position = driver.execute_script("return window.pageYOffset;")

        # Si la posición no cambia, significa que hemos llegado al final de la página
        if new_position == old_position:
            break

        # Recopilamos los productos
        titles_elements = driver.find_elements(By.CSS_SELECTOR, 'h3._text_f6lbl_1')
        prices_elements = driver.find_elements(By.CSS_SELECTOR, 'span.price__PriceText-sc-1nlvmq9-0')
        image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.image__StyledLazyLoadImage-sc-wislgi-0')


        if titles_elements and prices_elements and image_elements:
            print(f'Scraping data from {url}')
            for title_element, price_element, image_element in zip(titles_elements, prices_elements, image_elements):
                title = title_element.text.strip()  # Obtener el texto del nombre del producto
                price = price_element.text.strip()  # Obtener el texto del precio
                image_url = image_element.get_attribute('src')  # Obtener la URL de la imagen

                title = unidecode(title)

                # Verificamos si el producto ya está en la lista
                if {'title': title, 'price': price, 'image_url': image_url} not in products:
                    products.append({'title': title, 'price': price, 'image_url': image_url})
        else:
            print(f'No data found at {url}')

    return products

# Definir una función para ejecutar scrape_alcampo() en un hilo
def scrape_alcampo_thread():
    productsalcampo = scrape_alcampo()
    Utils.save_products_to_json(productsalcampo, 'productsalcampo')
    Utils.save_products_to_csv(productsalcampo, 'productsalcampo')
    print('Products from Alcampo saved to productsalcampo.json')

