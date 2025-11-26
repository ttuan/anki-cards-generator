"""Google Translate fallback for Vietnamese translations."""

from typing import Optional


class Translator:
    """Translate English words to Vietnamese using deep-translator."""

    def __init__(self):
        self._translator = None
        self._initialized = False

    def _init_translator(self):
        """Lazy initialization of translator."""
        if not self._initialized:
            try:
                from deep_translator import GoogleTranslator

                self._translator = GoogleTranslator(source="en", target="vi")
                self._initialized = True
            except ImportError:
                print("Warning: deep-translator not installed. Run: pip install deep-translator")
                self._initialized = True

    def translate_to_vietnamese(self, word: str) -> Optional[str]:
        """
        Translate an English word to Vietnamese.

        Args:
            word: English word to translate

        Returns:
            Vietnamese translation, or None on failure
        """
        if not word:
            return None

        self._init_translator()

        if not self._translator:
            return None

        try:
            result = self._translator.translate(word)
            return result
        except Exception as e:
            print(f"Translation error for '{word}': {e}")
            return None


if __name__ == "__main__":
    translator = Translator()
    test_words = ["absorb", "magnificent", "beautiful", "computer"]

    for word in test_words:
        translation = translator.translate_to_vietnamese(word)
        print(f"{word} -> {translation}")
