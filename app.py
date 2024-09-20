# Funcionalidades do aplicativo
'''
1. Entrada de dados
   O programa deve permitir que o usuário insira o nome do produto no terminal
2. Buscar em sites de venda de produtos
   Você deve definir dois sites de vendas de produtos(ex: mercadolivre e
   americanas) e criar o código necessário para ir até estes sites, pesquisar pelo
   produto que foi digitado
   O navegador não deve aparecer enquanto faz a busca(para evitar que o usuário
   quebre a automação)
3. Exibição do Menor Preço:
   Após realizado a busca, seu programa deve verificar qual site fornece o produto
   com o menor preço e depois filtrar pelo menor preço e retornar o link e preço do
   produto com o menor preço
4. Fechar o Navegador:
   Após a extração e comparação dos dados, o script deve fechar o navegador
   automaticamente.
5. (Bônus) - Opcional
   Criar uma interface gráfica para receber o input(entrada de dados) do usuário
'''
# Importando Bibliotéca e módulos webdriver e by
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# 1 Entrada de dados via terminal
produto = input('Digite o nome do produto que deseja buscar: ')

# Testando configuração para o Chrome
chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=pt-BR')
chrome_options.add_argument('--window-size=800,800')
chrome_options.add_argument('--disable-notifications')

# Caminho para o ChromeDriver
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Função para fechar popups
def fechar_popups():
    try:
        # Encontrar e fechar elementos de pop-up comuns caso tenha       
        popup_close_buttons = [
            ('CLASS_NAME', 'andes-modal__close'),
            ('CLASS_NAME', 'close-button'),
            ('CSS_SELECTOR', '[aria-label="Fechar"]'),
            ('XPATH', '//button[contains(text(), "Fechar")]'),
        ]

        for method, selector in popup_close_buttons:
            try:
                element = driver.find_element(getattr(By, method), selector)
                element.click()
                print(f"Pop-up fechado com {method}: {selector}")
                break  # Encerra se encontrar um pop-up
            except:
                continue  # Tenta o próximo método/selector

        print("Nenhum pop-up encontrado")
        
    except Exception as e:
        print("Erro ao tentar fechar pop-up", e)

# 2 Funções de busca
# Função para busca no Mercado Livre
def buscar_mercado_livre(produto):
    driver.get("https://www.mercadolivre.com.br")
    fechar_popups() 
    search_box = driver.find_element(By.NAME, 'as_word') 
    search_box.send_keys(produto)    
    search_box.submit()

    # Aguarda a página carregar e coleta o preço do item
    driver.implicitly_wait(10)
    try:
        # Capturando a parte inteira do preço
        preco_inteiro = driver.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
        
        # Capturar os centavos (se existirem)
        try:
            preco_centavos = driver.find_element(By.CLASS_NAME, 'andes-money-amount__cents').text
        except:
            preco_centavos = '00'  # Se não encontrar os centavos, assume que é '.00'

        # Montando o preço com o separador de centavos
        preco_completo = f"{preco_inteiro},{preco_centavos}"

        # Convertendo para float, preservando os separadores corretos
        preco_mercado_livre = float(preco_completo.replace('.', '').replace(',', '.'))
        
        # Capturando o link do produto
        link_mercado_livre = driver.find_element(By.CSS_SELECTOR, 'a.ui-search-link').get_attribute('href')
        
        return preco_mercado_livre, link_mercado_livre
    except Exception as e:
        print('Erro ao buscar no Mercado Livre', e)
        return None, None
    
# Função para busca na Amazon
def buscar_amazon(produto):
    driver.get("https://www.amazon.com.br")
    fechar_popups()  
    search_box = driver.find_element(By.ID, 'twotabsearchtextbox')    
    search_box.send_keys(produto)
    search_box.submit()

    driver.implicitly_wait(10)

    try:        
        preco_inteiro = driver.find_element(By.CLASS_NAME, 'a-price-whole').text     
        
        try:
            preco_centavos = driver.find_element(By.CLASS_NAME, 'a-price-fraction').text
        except:
            preco_centavos = '00'
      
        preco_completo = f"{preco_inteiro},{preco_centavos}"
        
        preco_amazon = float(preco_completo.replace('.', '').replace(',', '.'))
        
        # Capturar o link do produto na Amazon
        link_amazon = driver.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-no-outline').get_attribute('href')
        
        return preco_amazon, link_amazon

    except Exception as e:
        print('Erro ao buscar na Amazon:', e)
        return None, None

# Buscando o produto nos dois sites
preco_ml, link_ml = buscar_mercado_livre(produto)
preco_am, link_am = buscar_amazon(produto)

# 3 Comparando os preços e exibindo o menor preço
if preco_ml and preco_am:
   if preco_ml < preco_am:
      print(f'Menor preço encontrado no Mercado Livre: R${preco_ml}\nLink: {link_ml}')
   else:
    print(f'Menor preço encontrado na Amazon: R${preco_am}\nLink: {link_am}')
elif preco_ml:
   print(f'Somente o Mercado Livre retornou resultado: R${preco_ml}\nLink: {link_ml}')
elif preco_am:
   print(f'Somente as Amazon retornaram resultado: R${preco_am}\nLink: {link_am}')
else:
   print(f'Nenhum preço foi encontrado')     

# 4 Fechar o navegador após o input
driver.quit()