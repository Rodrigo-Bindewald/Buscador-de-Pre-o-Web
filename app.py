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

# Configurando o Chrome para rodar em modo "headless"(invisível)
'''chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--disable-extensions')'''

# Testando configuração para o Chrome
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--lang=pt-BR')
chrome_options.add_argument('--window-size=800,800')
chrome_options.add_argument('--disable-notifications')

# Caminho para o ChromeDriver
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Função para fechar popups
def fechar_popups():
    try:
        popup_close_button = driver.find_element(By.CLASS_NAME, 'some-close-class')  # Atualize com o seletor correto
        popup_close_button.click()
        print("Pop-up fechado")
    except Exception as e:
        print('Nenhum pop-up encontrado', e)


#  2 Funções de busca

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
        preco_mercado_livre = driver.find_element(By.CLASS_NAME, 'price-tag-fraction').text      
        link_mercado_livre = driver.find_element(By.CSS_SELECTOR, 'a.ui-search-link').get_attribute('href')
        return float(preco_mercado_livre.replace('.', '').replace(',', '.')), link_mercado_livre
    except Exception as e:
        print('Erro ao buscar no Mercado Livre', e) # e(objeto de exceção)
        return None, None        

# Função para busca nas Americanas
def buscar_americanas(produto):
    driver.get("https://www.americanas.com.br")
    fechar_popups()
    search_box = driver.find_element(By.NAME, 'conteudo')    
    search_box.send_keys(produto)
    search_box.submit()

    driver.implicitly_wait(10)
    try:
        preco_americanas = driver.find_element(By.CLASS_NAME, 'src__BestPrice-sc-1jvw02c-5').text
        link_americanas = driver.find_element(By.CSS_SELECTOR, 'a[href^="/produto"]').get_attribute('href')
        return float(preco_americanas.replace('R$', '').replace('.', '').replace(',', '.')), link_americanas
    except Exception as e:
        print('Erro ao buscar nas Americanas:', e)
        return None, None

# Buscando o produto nos dois sites
preco_ml, link_ml = buscar_mercado_livre(produto)
preco_am, link_am = buscar_americanas(produto)

# Comparando os preços
if preco_ml and preco_am:
   if preco_ml < preco_am:
      print(f'Menor preço encontrado no Mercado Livre: R${preco_ml}\nLink: {link_ml}')
   else:
    print(f'Menor preço encontrado nas Americanas: R${preco_am}\nLink: {link_am}')
elif preco_ml:
   print(f'Somente o Mercado Livre retornou resultado: R${preco_ml}\nLink: {link_ml}')
elif preco_am:
   print(f'Somente as Americanas retornaram resultado: R${preco_am}\nLink: {link_am}')
else:
   print(f'Nenhum preço foi encontraado')
      

# Fechar o navegador após o input
driver.quit()