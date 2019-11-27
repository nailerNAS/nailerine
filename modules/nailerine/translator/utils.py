from googletrans import Translator
from googletrans.models import Translated, Detected

from modules.utils import aiowrap


@aiowrap
def translate(text: str, dest: str = 'en', src: str = 'auto') -> Translated:
    return Translator().translate(text, dest, src)


@aiowrap
def detect(text: str) -> Detected:
    return Translator().detect(text)
