"""CSV input/output handling for Anki card generation."""

import csv
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterator, Optional


@dataclass
class InputWord:
    """Input word from CSV file."""

    keyword: str
    vietnamese: str = ""


@dataclass
class AnkiCard:
    """Output Anki card data."""

    no: str
    image: str = ""
    vietnamese: str = ""
    suggestion: str = ""
    keyword: str = ""
    transcription: str = ""
    explanation: str = ""
    sound: str = ""
    example: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary with proper field names for CSV."""
        return {
            "No": self.no,
            "Image": self.image,
            "Vietnamese": self.vietnamese,
            "Suggestion": self.suggestion,
            "Keyword": self.keyword,
            "Transcription": self.transcription,
            "Explanation": self.explanation,
            "Sound": self.sound,
            "Example": self.example,
        }


class CSVReader:
    """Read input CSV files."""

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def read_words(self) -> Iterator[InputWord]:
        """
        Read words from input CSV file.

        Expected format: Keyword,Vietnamese

        Yields:
            InputWord objects for each row
        """
        if not self.filepath.exists():
            raise FileNotFoundError(f"Input file not found: {self.filepath}")

        with open(self.filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                keyword = row.get("Keyword", "").strip()
                vietnamese = row.get("Vietnamese", "").strip()

                if keyword:
                    yield InputWord(keyword=keyword, vietnamese=vietnamese)


class CSVWriter:
    """Write output CSV files for Anki import."""

    OUTPUT_FIELDS = ["No", "Image", "Vietnamese", "Suggestion", "Keyword", "Transcription", "Explanation", "Sound", "Example"]

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def write_cards(self, cards: list[AnkiCard]) -> None:
        """
        Write Anki cards to CSV file.

        Args:
            cards: List of AnkiCard objects to write
        """
        with open(self.filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.OUTPUT_FIELDS)
            writer.writeheader()

            for card in cards:
                writer.writerow(card.to_dict())

        print(f"Written {len(cards)} cards to {self.filepath}")

    def append_card(self, card: AnkiCard) -> None:
        """
        Append a single card to the CSV file.

        Creates file with header if it doesn't exist.

        Args:
            card: AnkiCard object to append
        """
        file_exists = self.filepath.exists()

        with open(self.filepath, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.OUTPUT_FIELDS)

            if not file_exists:
                writer.writeheader()

            writer.writerow(card.to_dict())


if __name__ == "__main__":
    card = AnkiCard(
        no="absorb",
        image="absorb.jpg",
        vietnamese="hút/thấm",
        suggestion="_ b _ _ r b",
        keyword="absorb",
        explanation="{{c1::absorb}} - to take something in, especially gradually",
        sound="absorb.mp3",
        example="- Example 1\n- Example 2\n- Example 3",
    )

    print("Sample card dict:")
    print(card.to_dict())
