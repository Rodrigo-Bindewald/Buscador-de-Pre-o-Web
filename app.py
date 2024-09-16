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
# Importando Bibliotéca e configurando webdriver
from selenium import webdriver

# Criando uma instância do Seervice com o ChromeDriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configurando o Chrome para rodar em modo "headless"(invisível)
chrome_options = Options()
chrome_options.add_argument("--headless")

# Caminho para o ChromeDriver
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service)

# Acessando o Google para teste
driver.get("http://www.google.com")
print('Título da página:', driver.title)

# Fechar o navegador após o input
driver.quit()