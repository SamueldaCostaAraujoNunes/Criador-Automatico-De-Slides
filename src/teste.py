from PIL import Image, ImageFilter


def formata_imagem(origem, destino, width=1920, height=1080):
    original = Image.open(origem)
    width_original, height_original = original.size
    n_width = int((width_original * height) / height_original)
    dentro = original.resize((n_width, height))
    n_height = int((height_original * width) / width_original)
    fora = original.resize((1920, n_height))
    fora = fora.filter(ImageFilter.GaussianBlur(radius=6))
    altura_de_corte = (fora.size[1] - height) / 2
    area = (0, altura_de_corte, width, altura_de_corte + height)
    cropped_img = fora.crop(area)
    largura_de_corte = int((width - dentro.size[0]) / 2)
    cropped_img.paste(dentro, (largura_de_corte, 0))
    cropped_img.save(destino)


formata_imagem(
        "Images\\4.jpg",
        "Images\\4-tratado.jpg")
