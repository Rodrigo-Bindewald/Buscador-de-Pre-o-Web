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
chrome_options = Options()
chrome_options.add_argument("--headless")

# Caminho para o ChromeDriver
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service)

# Acessando o Google para teste
driver.get("http://www.google.com")
print('Título da página:', driver.title)

#  2 Funções de busca

# Função para busca no Mercado Livre
def busca_mercado_livre(produto):
    driver.get("https://www.mercadolivre.com.br")
    pass

# Função para busca nas Americanas
def busca_americanas(produto):
    driver.get("https://www.americanas.com.br")
    pass

# Fechar o navegador após o input
driver.quit()