from googleapiclient.discovery import build
from secrets import API_KEY_GOOGLE_SEARCH, SEARCH_ENGINE_ID
import json


class Imagem():
    def __init__(self):
        self.load()
        self.inclui_imagens()
        self.save()
        pass

    def google_search(self, search_term, **kwargs):
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
        sentences = self.dados["sentences"]
        tema = self.dados["input"]["temaCentral"]
        n_sentences = []
        for sentence in sentences:
            keyword = sentence["keywords"][0]
            search = tema.title() + " " + keyword
            print(search)
            sentence["images"] = self.google_search(
                search,
                num=3,
                #imgSize="HUGE"
                )
            n_sentences.append(sentence)
        self.dados["sentences"] = n_sentences

    def save(self):
        """
        Salva o conteudo tratado no documento,
        dadosSentences.json
        """
        with open('Documents\\dados.json', 'w',
                  encoding='utf-8') as outfile:
            json.dump(self.dados, outfile, indent=2,
                      ensure_ascii=False)

    def load(self) -> dict:
        """
        Importa os dados de dadosSentences.json
        """
        with open('Documents\\dados.json', 'r',
                  encoding='utf-8') as j:
            self.dados = json.load(j)


if __name__ == '__main__':
    bot_image = Imagem()
    # print(bot_image.google_search("fortrek k7"), num=2)