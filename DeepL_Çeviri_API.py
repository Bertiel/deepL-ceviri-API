import requests
from docx import Document
import os

# API anahtarınızı tırnakların içine yazın.
DEEPL_API_KEY = ''

#Özelleştirilmiş sözlük, belli bir ingilizce kelimeyi istediğiniz şekilde çevirmesini sağlayabilirsiniz.
custom_dictionary = {
    "still": "hâlâ",
    "wind": "rüzgâr",
}

def apply_custom_dictionary(text, dictionary):

    for key, value in dictionary.items():
        text = text.replace(key, value)
    return text

#Hedef Dil, hangi dile çevirmek istiyorsanız onun dil kodunu girin.
def translate_text(text, target_language='TR'):

    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key " + DEEPL_API_KEY
    }
    data = {
        "text": text,
        "target_lang": target_language
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        translated_text = response.json()["translations"][0]["text"]
        return translated_text
    else:
        #Hatayla karşılaşırsanız burada kod numarasını internete yazarak sorunun detayını öğrenebilirsiniz.
        raise Exception(f"Çeviri işleminiz başarısız oldu: {response.status_code}, {response.text}")

#Hedef Dil, hangi dile çevirmek istiyorsanız onun dil kodunu girin.
def translate_paragraph(paragraph, target_language='TR'):

    paragraph = apply_custom_dictionary(paragraph, custom_dictionary)
    
    lines = paragraph.split('\n')
    translated_lines = [translate_text(line, target_language) for line in lines if line.strip() != '']
    return '\n'.join(translated_lines)


if __name__ == "__main__":
    #Çevirinin içeriğini aşağıya, tırnakların içine yapıştırın.
    metin = ""

    hedef_dil = "TR"
    paragraflar = metin.split('\n\n')

    cevrilen_paragraflar = [translate_paragraph(paragraph, hedef_dil) for paragraph in paragraflar]

    cevrilen_metin = '\n\n'.join(cevrilen_paragraflar)

#Çeviri masaüstünüze docx uzantısıyla kaydolacaktır.
desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
file_path = os.path.join(desktop_path, 'ceviri.docx')
doc = Document()
doc.add_paragraph(cevrilen_metin)
doc.save(file_path)

print("Çeviri işlemi tamamlandı. Dosya docx uzantısıyla masaüstüne kaydedilmiştir.")
