# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json


class Texto:
    """
    A classe Texto é responsável por criar, tratar, 
    interpretar e separar os textos a respeito do tema central.
    """
    def __init__(self):
        """
        Inicializa a classe Texto
        """
        self.keywords = ["O que é?", "Para que serve?", "Como funciona?",
                         "Exemplos", "Impactos", "Causas",
                         "Consequências"]
        self.dados = self.importa_dados()

    def importa_dados(self) -> dict:
        """
        Importa os dados de input do usuário
        """
        with open('Documents\\dadosInput.json', 'r') as j:
            json_data = json.load(j)
            return json_data

    def pesquisa_artigos(self) -> None:
        """
        Pesquisa o tema central  no Google Académico, cria um dict
        contendo o nome do artigo e o link para o download.
        """
        headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) \
                           AppleWebKit/601.3.9 (KHTML, like Gecko) \
                           Version/9.0.2 Safari/601.3.9'}

        artigos_obj: dict = {}
        num_page: int = 0
        while len(artigos_obj.values()) < 15:
            url = self.gerar_url(num_page)
            try:
                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.content, 'html.parser')
                artigos = soup.find('div', id="gs_res_ccl_mid")
                artigos = artigos.find_all('div', {"class": "gs_r gs_or gs_scl"})

                for artigo in artigos:
                    titulo = artigo.h3.a.get_text()
                    link = artigo.a['href']
                    artigos_obj[titulo] = link

            except AttributeError:
                pass

            num_page += 1

        if artigos_obj:
            self.save(artigos_obj)

    def gerar_url(self, index: int) -> str:
        """
        Pesquisa o tema central no JSON de inputs
        e cria um URL de pesquisa no Google Académico.
        """
        query = self.dados["temaCentral"]
        query = query.strip().lower().replace(' ', '+')
        url = f"https://scholar.google.com.br/scholar?start={index}&q={query}&hl=pt-BR&as_sdt=0,5"
        return url

    def save(self, artigos: dict) -> bool:
        """
        Esta função salva os artigos em um JSON.
        """
        try:
            with open('Documents\\artigos.json', 'w') as outfile:
                json.dump(artigos, outfile, indent=2, ensure_ascii=False)
            return True

        except Exception as e:
            print("Erro na função save: ", e)
            return False


if __name__ == '__main__':
    texto = Texto()
    texto.pesquisa_artigos()
