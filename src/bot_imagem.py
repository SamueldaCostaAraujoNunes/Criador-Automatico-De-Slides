from googleapiclient.discovery import build
from secrets import API_KEY_GOOGLE_SEARCH, SEARCH_ENGINE_ID
import json
from tqdm import tqdm
import requests
from PIL import Image, ImageFilter


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
        self.pbar = tqdm(desc="Robô de Imagem: ", total=5)
        self.progress_bar(self.load)
        self.progress_bar(self.inclui_imagens)
        self.progress_bar(self.save)
        self.progress_bar(self.baixa_imagens)
        self.progress_bar(self.trata_imagens)
        self.pbar.close()

    def progress_bar(self, function):
        function()
        self.pbar.update()

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
            imgColorType='color',
            # rights="cc_publicdomain",
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
            sentence["images"] = self.google_search(
                search,
                num=3,
                # imgSize="HUGE,"
                # imgDominantColor="RED", # Cor predominante
                )
            n_sentences.append(sentence)
        self.dados["sentences"] = n_sentences

    def baixa_imagens(self):
        """
        Baixa as imagens da estrutura de dados.
        """
        lista_urls = [link["images"] for link in self.dados["sentences"]]
        sentence = 0
        baixados = []
        for urls in lista_urls:
            not_download = True
            cont = 0
            while not_download:
                try:
                    url = urls[cont]
                    if url not in baixados:
                        r = requests.get(url)
                        with open(f'Images\\{sentence}.jpg', 'wb') as f:
                            f.write(r.content)
                        not_download = False
                        baixados.append(url)
                    else:
                        raise Exception('Já existe esta imagem')
                except Exception:
                    not_download = True
                cont += 1
            sentence += 1

    def trata_imagens(self):
        for imagem_index in range(len(self.dados["sentences"])):
            self.formata_imagem(
                f"Images\\{imagem_index}.jpg",
                f"Images\\{imagem_index}-tratado.jpg")

    def formata_imagem(self, origem, destino, width=1920, height=1080):
        original = Image.open(origem)
        width_original, height_original = original.size
        n_width = int((width_original * height) / height_original)
        dentro = original.resize((n_width, height))
        n_height = int((height_original * width) / width_original)
        fora = original.resize((1920, n_height))
        fora = fora.filter(ImageFilter.GaussianBlur(radius=4))
        altura_de_corte = (fora.size[1] - height) / 2
        area = (0, altura_de_corte, width, altura_de_corte + height)
        cropped_img = fora.crop(area)
        largura_de_corte = int((width - dentro.size[0]) / 2)
        cropped_img.paste(dentro, (largura_de_corte, 0))
        cropped_img.save(destino)

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
