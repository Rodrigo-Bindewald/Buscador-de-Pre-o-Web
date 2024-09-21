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
import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import webbrowser

# 1-Entrada de dados
# Função que será chamada ao clicar no botão "Buscar"
def buscar():
    produto = entry_produto.get()  # Captura o nome do produto inserido
    if not produto:
        messagebox.showwarning("Aviso", "Por favor, insira o nome do produto.")
        return
    
    # Configuração do Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--lang=pt-BR')
    chrome_options.add_argument('--window-size=800,800')
    chrome_options.add_argument('--disable-notifications')
    
    # Caminho para o ChromeDriver
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Função para verificar se o elemento existe
    def element_exists(driver, by, selector):
        try:
            WebDriverWait(driver, 5).until(lambda d: d.find_element(by, selector))
            return True
        except:
            return False

    # Função para fechar pop-ups, caso o elemento exista a função é ativada
    def fechar_popups(driver, ativo=False):
        if not ativo:
            return  # Não faz nada se o fechamento de pop-ups estiver desativado

        try:
            popup_close_buttons = [
                ('CLASS_NAME', 'andes-modal__close'),
                ('CLASS_NAME', 'close-button'),
                ('CSS_SELECTOR', '[aria-label="Fechar"]'),
                ('XPATH', '//button[contains(text(), "Fechar")]'),
            ]
            
            for method, selector in popup_close_buttons:
                if element_exists(driver, getattr(By, method), selector):
                    try:
                        element = driver.find_element(getattr(By, method), selector)
                        element.click()
                        break  # Sai do loop se o popup foi fechado com sucesso
                    except Exception as e:
                        print(f"Erro ao tentar clicar no botão de fechar: {e}")
                        continue
        except Exception as e:
            print("Erro ao tentar fechar pop-up", e)

    # Função de busca no Mercado Livre
    def buscar_mercado_livre(produto):
        driver.get("https://www.mercadolivre.com.br")
        fechar_popups(driver)
        search_box = driver.find_element(By.NAME, 'as_word')
        search_box.send_keys(produto)
        search_box.submit()

        driver.implicitly_wait(10)
        # Captura o valor e centavos e monta o valor no formato correto para exibir no resultado
        try:
            preco_inteiro = driver.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text
            try:
                preco_centavos = driver.find_element(By.CLASS_NAME, 'andes-money-amount__cents').text
            except:
                preco_centavos = '00'
            preco_completo = f"{preco_inteiro},{preco_centavos}"
            preco_mercado_livre = float(preco_completo.replace('.', '').replace(',', '.'))
            link_mercado_livre = driver.find_element(By.CSS_SELECTOR, 'a.ui-search-link').get_attribute('href')
            return preco_mercado_livre, link_mercado_livre
        except Exception as e:
            print('Erro ao buscar no Mercado Livre', e)
            return None, None

    # Função de busca na Amazon
    def buscar_amazon(produto):
        driver.get("https://www.amazon.com.br")
        fechar_popups(driver)
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
            link_amazon = driver.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-no-outline').get_attribute('href')
            return preco_amazon, link_amazon
        except Exception as e:
            print('Erro ao buscar na Amazon:', e)
            return None, None

    # Buscando o produto nos dois sites
    preco_ml, link_ml = buscar_mercado_livre(produto)
    preco_am, link_am = buscar_amazon(produto)

    # Comparando e exibindo o menor preço na interface gráfica
    if preco_ml and preco_am:
        if preco_ml < preco_am:
            result = f"Menor preço no Mercado Livre: R${preco_ml}"
            link_final = link_ml
        else:
            result = f"Menor preço na Amazon: R${preco_am}"
            link_final = link_am
    elif preco_ml:
        result = f"Somente o Mercado Livre retornou resultado: R${preco_ml}"
        link_final = link_ml
    elif preco_am:
        result = f"Somente a Amazon retornou resultado: R${preco_am}"
        link_final = link_am
    else:
        result = "Nenhum preço foi encontrado."
        link_final = None

    # Fecha o navegador
    driver.quit()

    # Exibe uma nova janela com os botões para acessar o link ou cancelar
    mostrar_resultado(result, link_final)

# Função que exibe o resultado e os botões "Ir para o Link" e "Cancelar"
def mostrar_resultado(mensagem, link):
    # Cria uma nova janela
    resultado_janela = tk.Toplevel(root)
    resultado_janela.title("Resultado da Busca")
    resultado_janela.geometry('400x200')

    # Calcula a posição para centralizar a janela de resultado sobre a janela principal
    x = root.winfo_rootx() + (root.winfo_width() // 2) - 200
    y = root.winfo_rooty() + (root.winfo_height() // 2) - 100
    resultado_janela.geometry(f"400x200+{x}+{y}")

    # Exibe a mensagem com o preço encontrado
    label_resultado = tk.Label(resultado_janela, text=mensagem, wraplength=350)
    label_resultado.pack(pady=20)

    # Botão para abrir o link no navegador
    if link:
        btn_ir_link = tk.Button(resultado_janela, text="Ir para o Link", command=lambda: webbrowser.open(link))
        btn_ir_link.pack(pady=5)

    # Botão para fechar a janela
    btn_fechar = tk.Button(resultado_janela, text="Fechar", command=resultado_janela.destroy)
    btn_fechar.pack(pady=5)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Buscador de Preços")
root.geometry('600x200')

# Label e campo de entrada para o produto
label_produto = tk.Label(root, text="Nome do Produto:")
label_produto.pack(pady=20)

entry_produto = tk.Entry(root, width=50)
entry_produto.pack(pady=10)

# Botão para iniciar a busca
btn_buscar = tk.Button(root, text="Buscar Menor Preço", command=buscar)
btn_buscar.pack(pady=20)

# Executa a janela principal
root.mainloop()
