from googleapiclient.discovery import build
from secrets import API_KEY_GOOGLE_SEARCH, SEARCH_ENGINE_ID
import json
from tqdm import tqdm
import requests


class Imagem():
    """
    A classe Imagem é responsável por pesquisar,
    baixar e tratar qualquer imagem
    utilizada no programa.
    """
    def __init__(self):
        """
        Inicializa a classe Imagem
        """
        self.pbar = tqdm(desc="Robô de Imagem: ", total=4)
        self.load()
        self.pbar.update()
        self.inclui_imagens()
        self.pbar.update()
        self.baixa_imagens()
        self.pbar.update()
        self.save()
        self.pbar.update()
        self.pbar.close()

    def google_search(self, search_term, **kwargs):
        """
        Acessa a API do Google Custom Search,
        e retorna uma lista de links de imagens
        relacionadas.
        """
        service = build("customsearch", "v1",
                        developerKey=API_KEY_GOOGLE_SEARCH)
        res = service.cse().list(
            q=search_term,
            cx=SEARCH_ENGINE_ID,
            searchType='image',
            **kwargs).execute()

        images_link = [items["link"] for items in res["items"]]
        return images_link

    def inclui_imagens(self):
        """
        Insere a lista de links,
        das imagens relacionadas
        a cada sentenças
        """
        sentences = self.dados["sentences"]
        tema = self.dados["input"]["temaCentral"]
        n_sentences = []
        for sentence in sentences:
            keyword = sentence["keywords"][0]
            search = tema.title() + " " + keyword
            print(search)
            sentence["images"] = self.google_search(
                search,
                num=2,
                # imgSize="HUGE"
                )
            n_sentences.append(sentence)
        self.dados["sentences"] = n_sentences

    def baixa_imagens(self):
        """
        Baixa as imagens da estrutura de dados.
        """
        lista_urls = [link["images"] for link in self.dados["sentences"]]
        sentence = 0
        for urls in lista_urls:
            not_download = True
            cont = 0
            while not_download:
                try:
                    url = urls[cont]
                    r = requests.get(url)
                    with open(f'Images\\{sentence}.jpg', 'wb') as f:
                        f.write(r.content)
                    not_download = False
                except Exception:
                    not_download = True
                    cont += 1
            sentence += 1

    def save(self):
        """
        Salva o conteudo tratado no documento,
        dados.json
        """
        with open('Documents\\dados.json', 'w',
                  encoding='utf-8') as outfile:
            json.dump(self.dados, outfile, indent=2,
                      ensure_ascii=False)

    def load(self):
        """
        Importa os dados de dados.json
        """
        with open('Documents\\dados.json', 'r',
                  encoding='utf-8') as j:
            self.dados = json.load(j)


if __name__ == '__main__':
    bot_image = Imagem()
    # print(bot_image.google_search("fortrek k7"), num=2)
