import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal")
    driver.fullscreen_window()

    # Espera até que o campo de busca esteja disponível
    search = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "search"))  # Verifique o seletor correto
    )
    search.send_keys("senac")

finally:
    driver.quit()