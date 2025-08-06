from googletrans import Translator

translator = Translator()

translated = translator.translate("Hello world", dest='ko').text
print(translated)  # "안녕하세요 세계" 혹은 비슷한 번역 결과 나와야 함
