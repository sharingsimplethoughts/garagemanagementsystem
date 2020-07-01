"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
# from google.cloud import translate_v2 as translate

# def translate_text(text,target='ar'):
#     translate_client = translate.Client()

#     if isinstance(text, six.binary_type):
#         text = text.decode('utf-8')

#     # Text can also be a sequence of strings, in which case this method
#     # will return a sequence of results for each text.
#     result = translate_client.translate(
#         text, target_language=target)

#     print(u'Text: {}'.format(result['input']))
#     print(u'Translation: {}'.format(result['translatedText']))
#     print(u'Detected source language: {}'.format(
#         result['detectedSourceLanguage']))


#translate(text, dest='en', src='auto')
#----------------------------------------
from googletrans import Translator
translator = Translator()
def translate_text_ar(text,target='ar'):
    # translations = translator.translate(['The quick brown fox', 'jumps over', 'the lazy dog'], dest='ko')
    # src = translator.detect(text[0])
    # if src.lang=='ar':
    #     target='en'
    # elif src.lang=='en':
    #     target='ar'
    # else:
    #     target=0
    translations = translator.translate(text, dest=target)
    print(translations)
    return translations
    # for translation in translations:
    #     print(translation.origin, ' -> ', translation.text)
