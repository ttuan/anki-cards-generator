"""Download sound files from URLs."""

import os
import requests
from pathlib import Path
from typing import Optional


class SoundDownloader:
    """Download and manage sound files."""

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "audio/webm,audio/ogg,audio/wav,audio/*;q=0.9,application/ogg;q=0.7,video/*;q=0.6,*/*;q=0.5",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://dictionary.cambridge.org/",
    }

    def __init__(self, output_dir: str = "output/sounds", suffix: str = "_auto_tool"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.suffix = suffix

    def download(self, url: str, filename: str) -> Optional[str]:
        """
        Download sound file from URL.

        Args:
            url: URL of the sound file
            filename: Name for the saved file (without extension)

        Returns:
            Filename of the downloaded file, or None on failure
        """
        if not url:
            return None

        ext = self._get_extension(url)
        full_filename = f"{filename}{self.suffix}{ext}"
        filepath = self.output_dir / full_filename

        if filepath.exists():
            print(f"Sound file already exists: {full_filename}")
            return full_filename

        try:
            response = requests.get(url, headers=self.HEADERS, timeout=30, stream=True)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Downloaded sound: {full_filename}")
            return full_filename

        except requests.RequestException as e:
            print(f"Error downloading sound from {url}: {e}")
            return None

    def _get_extension(self, url: str) -> str:
        """Extract file extension from URL."""
        if ".mp3" in url.lower():
            return ".mp3"
        elif ".wav" in url.lower():
            return ".wav"
        elif ".ogg" in url.lower():
            return ".ogg"
        return ".mp3"

    def get_filepath(self, filename: str) -> Path:
        """Get full filepath for a sound file."""
        return self.output_dir / filename


if __name__ == "__main__":
    downloader = SoundDownloader()
    test_url = "https://dictionary.cambridge.org/us/media/english/us_pron/e/eus/eus70/eus70027.mp3"
    result = downloader.download(test_url, "absorb")
    print(f"Result: {result}")
