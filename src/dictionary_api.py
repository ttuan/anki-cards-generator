"""Dictionary API client for fetching word definitions and pronunciations."""

import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class WordInfo:
    """Structured word information from dictionary API."""

    word: str
    pronunciation_url: Optional[str] = None
    transcription: Optional[str] = None
    definition: Optional[str] = None
    examples: list[str] = None

    def __post_init__(self):
        if self.examples is None:
            self.examples = []


class DictionaryAPIClient:
    """Client for the dictionary API."""

    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url.rstrip("/")

    def get_word_info(self, word: str) -> Optional[WordInfo]:
        """
        Fetch word information from the dictionary API.

        Args:
            word: The English word to look up

        Returns:
            WordInfo object with pronunciation, definition, and examples
        """
        url = f"{self.base_url}/api/dictionary/en/{word}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            return self._parse_response(word, data)
        except requests.RequestException as e:
            print(f"Error fetching word '{word}': {e}")
            return None

    def _parse_response(self, word: str, data: dict) -> WordInfo:
        """Parse API response into WordInfo object."""
        pronunciation_url = None
        transcription = None
        definition = None
        examples = []

        pronunciations = data.get("pronunciation", [])
        for pron in pronunciations:
            if pron.get("lang") == "us":
                pronunciation_url = pron.get("url")
                transcription = pron.get("pron")
                break

        if not pronunciation_url and pronunciations:
            pronunciation_url = pronunciations[0].get("url")
            transcription = pronunciations[0].get("pron")

        definitions = data.get("definition", [])
        if definitions:
            first_def = definitions[0]
            definition = first_def.get("text", "").strip().rstrip(":")

            for def_item in definitions:
                def_examples = def_item.get("example", [])
                for ex in def_examples:
                    ex_text = ex.get("text", "").strip()
                    if ex_text and len(examples) < 3:
                        examples.append(ex_text)

        return WordInfo(
            word=word,
            pronunciation_url=pronunciation_url,
            transcription=transcription,
            definition=definition,
            examples=examples,
        )

    def format_explanation(self, word: str, definition: str) -> str:
        """
        Format explanation with cloze syntax for Anki.

        Args:
            word: The English word
            definition: The definition text

        Returns:
            Formatted string like "{{c1::word}} - definition"
        """
        if not definition:
            return f"{{{{c1::{word}}}}}"

        return f"{{{{c1::{word}}}}} - {definition}"

    def format_examples(self, examples: list[str]) -> str:
        """
        Format examples as bullet list for Anki.

        Args:
            examples: List of example sentences

        Returns:
            Formatted string with bullet points
        """
        if not examples:
            return ""

        return "<br>".join(f"- {ex}" for ex in examples[:3])


if __name__ == "__main__":
    client = DictionaryAPIClient()
    info = client.get_word_info("absorb")

    if info:
        print(f"Word: {info.word}")
        print(f"Transcription: {info.transcription}")
        print(f"Sound URL: {info.pronunciation_url}")
        print(f"Definition: {info.definition}")
        print(f"Examples: {info.examples}")
        print(f"\nFormatted explanation: {client.format_explanation(info.word, info.definition)}")
        print(f"\nFormatted examples:\n{client.format_examples(info.examples)}")
