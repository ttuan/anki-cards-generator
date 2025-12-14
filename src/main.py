#!/usr/bin/env python3
"""Main orchestration script for Anki card generation."""

import argparse
import sys
from pathlib import Path

from csv_handler import CSVReader, CSVWriter, AnkiCard
from dictionary_api import DictionaryAPIClient
from sound_downloader import SoundDownloader
from image_downloader import PexelsImageDownloader
from translator import Translator
from suggestion import generate_suggestion_deterministic


class AnkiCardGenerator:
    """Generate Anki cards from input CSV."""

    def __init__(
        self,
        input_file: str,
        output_file: str = "output.csv",
        sounds_dir: str = "output/sounds",
        images_dir: str = "output/images",
        dictionary_url: str = "https://dictionary-api.eliaschen.dev",
    ):
        self.csv_reader = CSVReader(input_file)
        self.csv_writer = CSVWriter(output_file)
        self.dictionary = DictionaryAPIClient(dictionary_url)
        self.sound_downloader = SoundDownloader(sounds_dir)
        self.image_downloader = PexelsImageDownloader(images_dir)
        self.translator = Translator()

    def generate(self) -> list[AnkiCard]:
        """
        Generate Anki cards from input CSV.

        Returns:
            List of generated AnkiCard objects
        """
        cards = []
        skipped = []

        for input_word in self.csv_reader.read_words():
            print(f"\nProcessing: {input_word.keyword}")

            word_info = self.dictionary.get_word_info(input_word.keyword)

            if not word_info or not word_info.definition:
                print(f"  -> Skipped (not found in dictionary)")
                skipped.append(input_word.keyword)
                continue

            card = self._process_word(input_word, word_info)
            cards.append(card)

        self.csv_writer.write_cards(cards)

        if skipped:
            print(f"\n--- Skipped {len(skipped)} phrases (not in dictionary) ---")
            for word in skipped:
                print(f"  - {word}")
            self._write_skipped_log(skipped)

        return cards

    def _write_skipped_log(self, skipped: list[str]) -> None:
        """Write skipped words to a log file for manual review."""
        log_path = Path("skipped_words.txt")
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("# Words/phrases not found in dictionary\n")
            f.write("# Add these manually or review later\n\n")
            for word in skipped:
                f.write(f"{word}\n")
        print(f"Skipped words saved to: {log_path}")

    def _process_word(self, input_word, word_info) -> AnkiCard:
        """Process a single word and generate an Anki card."""
        keyword = input_word.keyword
        vietnamese = input_word.vietnamese

        if not vietnamese:
            vietnamese = self.translator.translate_to_vietnamese(keyword) or ""

        sound_file = ""
        if word_info.pronunciation_url:
            sound_file = self.sound_downloader.download(word_info.pronunciation_url, keyword) or ""

        image_file = self.image_downloader.search_and_download(keyword) or ""

        suggestion = generate_suggestion_deterministic(keyword)

        transcription = word_info.transcription or ""
        explanation = self.dictionary.format_explanation(keyword, word_info.definition)
        examples = self.dictionary.format_examples(word_info.examples)

        # Format for Anki media syntax
        image_anki = f'<img src="{image_file}">' if image_file else ""
        sound_anki = f"[sound:{sound_file}]" if sound_file else ""

        return AnkiCard(
            no=keyword,
            image=image_anki,
            vietnamese=vietnamese,
            suggestion=suggestion,
            keyword=keyword,
            transcription=transcription,
            explanation=explanation,
            sound=sound_anki,
            example=examples,
        )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate Anki cards from vocabulary CSV")
    parser.add_argument("input", help="Input CSV file path")
    parser.add_argument("-o", "--output", default="output.csv", help="Output CSV file path")
    parser.add_argument("--sounds-dir", default="output/sounds", help="Directory for sound files")
    parser.add_argument("--images-dir", default="output/images", help="Directory for image files")
    parser.add_argument(
        "--dictionary-url", default="https://dictionary-api.eliaschen.dev", help="Dictionary API base URL"
    )

    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    generator = AnkiCardGenerator(
        input_file=args.input,
        output_file=args.output,
        sounds_dir=args.sounds_dir,
        images_dir=args.images_dir,
        dictionary_url=args.dictionary_url,
    )

    try:
        cards = generator.generate()
        print(f"\nSuccess! Generated {len(cards)} Anki cards.")
        print(f"Output file: {args.output}")
        print(f"Sound files: {args.sounds_dir}/")
        print(f"Image files: {args.images_dir}/")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
