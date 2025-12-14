"""Download images from Pexels API."""

import os
import time
import requests
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class PexelsImageDownloader:
    """Download images from Pexels API."""

    def __init__(self, output_dir: str = "output/images", api_key: str = None, suffix: str = "_auto_tool"):
        load_dotenv()

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.api_key = api_key or os.getenv("PEXELS_API_KEY")
        self.base_url = "https://api.pexels.com/v1"
        self.suffix = suffix

        if not self.api_key:
            print("Warning: PEXELS_API_KEY not found in environment")

    def search_and_download(self, keyword: str, filename: str = None) -> Optional[str]:
        """
        Search for an image by keyword and download it.

        Args:
            keyword: Search keyword for the image
            filename: Name for the saved file (without extension). Defaults to keyword.

        Returns:
            Filename of the downloaded image, or None on failure
        """
        if not self.api_key:
            print("Pexels API key not configured")
            return None

        filename = filename or keyword
        image_url = self._search_image(keyword)

        if not image_url:
            return None

        return self._download_image(image_url, filename)

    def _search_image(self, keyword: str, max_retries: int = 3, initial_delay: int = 2) -> Optional[str]:
        """
        Search Pexels for an image matching the keyword.

        Implements rate limit handling with exponential backoff.

        Args:
            keyword: Search keyword
            max_retries: Maximum number of retry attempts for rate limit errors
            initial_delay: Initial delay in seconds before first retry
        """
        url = f"{self.base_url}/search"
        headers = {"Authorization": self.api_key}
        params = {"query": keyword, "per_page": 1, "orientation": "square"}

        for attempt in range(max_retries + 1):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                photos = data.get("photos", [])
                if photos:
                    return photos[0]["src"]["medium"]

                print(f"No images found for keyword: {keyword}")
                return None

            except requests.HTTPError as e:
                if e.response.status_code == 429:
                    if attempt < max_retries:
                        delay = initial_delay * (2 ** attempt)
                        print(f"Rate limit hit for '{keyword}'. Waiting {delay}s before retry ({attempt + 1}/{max_retries})...")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"Rate limit exceeded for '{keyword}' after {max_retries} retries. Skipping.")
                        return None
                else:
                    print(f"HTTP error searching Pexels for '{keyword}': {e}")
                    return None

            except requests.RequestException as e:
                print(f"Error searching Pexels for '{keyword}': {e}")
                return None

        return None

    def _download_image(self, url: str, filename: str) -> Optional[str]:
        """Download image from URL."""
        ext = self._get_extension(url)
        full_filename = f"{filename}{self.suffix}{ext}"
        filepath = self.output_dir / full_filename

        if filepath.exists():
            print(f"Image already exists: {full_filename}")
            return full_filename

        try:
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Downloaded image: {full_filename}")
            return full_filename

        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    def _get_extension(self, url: str) -> str:
        """Extract file extension from URL."""
        url_lower = url.lower().split("?")[0]

        if url_lower.endswith(".jpg") or url_lower.endswith(".jpeg"):
            return ".jpg"
        elif url_lower.endswith(".png"):
            return ".png"
        elif url_lower.endswith(".webp"):
            return ".webp"
        return ".jpg"

    def get_filepath(self, filename: str) -> Path:
        """Get full filepath for an image file."""
        return self.output_dir / filename


if __name__ == "__main__":
    downloader = PexelsImageDownloader()
    result = downloader.search_and_download("absorb")
    print(f"Result: {result}")
