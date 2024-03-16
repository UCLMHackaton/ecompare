from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from unidecode import unidecode
import Utils

import time
def scrape_carrefour():
    pages = 42
    products = []

    # Configurar el controlador de Selenium (ChromeDriver)
    service = Service('chromedriver.exe', port=9515)
    options = Options()

    driver = webdriver.Chrome(service=service, options=options)

    for page in range(pages):
        offset = page * 24
        url = f'https://www.carrefour.es/supermercado/la-despensa/alimentacion/cat20009/c?offset={offset}'
        driver.get(url)

        # Definimos el número máximo de desplazamientos
        max_scrolls = 80

        # Desplazamos la página hacia abajo en incrementos más pequeños
        for _ in range(max_scrolls):
            # Obtenemos la posición actual de la página antes del desplazamiento
            old_position = driver.execute_script("return window.pageYOffset;")

            # Desplazamos hacia abajo
            driver.execute_script("window.scrollBy(0, 1000);")

            # Esperamos un breve momento para que se carguen los elementos
            time.sleep(0.3)

            # Obtenemos la posición de la página después del desplazamiento
            new_position = driver.execute_script("return window.pageYOffset;")

            # Si la posición no cambia, significa que hemos llegado al final de la página
            if new_position == old_position:
                break

            # Recopilamos los productos
            titles_elements = driver.find_elements(By.CSS_SELECTOR, 'h2.product-card__title')
            prices_elements = driver.find_elements(By.CSS_SELECTOR, 'span.product-card__price')
            image_elements = driver.find_elements(By.CSS_SELECTOR, 'img.product-card__image')


            if titles_elements and prices_elements and image_elements:
                print(f'Scraping data from {url}')
                for title_element, price_element, image_element in zip(titles_elements, prices_elements, image_elements):
                    title = title_element.text.strip()  # Obtener el texto del nombre del producto
                    price = price_element.text.strip()  # Obtener el texto del precio
                    image_url = image_element.get_attribute('src')  # Obtener la URL de la imagen

                    title = unidecode(title)

                    if {'title': title, 'price': price, 'image_url': image_url} not in products:
                        if image_url.startswith('https://static.carrefour.es/hd_350x_/img_pim_food/'):
                            products.append({'title': title, 'price': price, 'image_url': image_url})

            else:
                print(f'No data found at {url}')

    return products

# Definir una función para ejecutar scrape_carrefour() en un hilo
def scrape_carrefour_thread():
    productscarrefour = scrape_carrefour()
    Utils.save_products_to_json(productscarrefour, 'productscarrefour')
    Utils.save_products_to_csv(productscarrefour, 'productscarrefour')
    print('Products from Carrefour saved to productscarrefour.json')




