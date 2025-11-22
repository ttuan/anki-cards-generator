# Anki Cards Generator

A Python CLI tool that automates English vocabulary Anki card creation from CSV input. It fetches word definitions from Cambridge Dictionary, downloads pronunciation audio and images, and outputs Anki-ready CSV files.

## Features

- Fetch word definitions, pronunciations, and examples from Cambridge Dictionary API
- Download US pronunciation audio (MP3)
- Download related images from Pexels
- Auto-translate to Vietnamese using Google Translate (if not provided)
- Generate cloze-style hints (e.g., "absorb" → "_ b _ _ r b")
- Output Anki-importable CSV with all fields

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Pexels API Key

```bash
cp .env.example .env
```

Edit `.env` and add your Pexels API key (get one free at https://www.pexels.com/api/):

```
PEXELS_API_KEY=your_api_key_here
```

## Usage

### 1. Prepare Input CSV

Create a CSV file with your vocabulary words:

```csv
Keyword,Vietnamese
abuse,"lăng mạ, xỉ nhục"
acquire,
magnificent,tráng lệ
```

- `Keyword`: Required - the English word
- `Vietnamese`: Optional - will be auto-translated if empty

### 2. Generate Anki Cards

```bash
python src/main.py input.csv -o output.csv
```

Options:
```
-o, --output         Output CSV file path (default: output.csv)
--sounds-dir         Directory for sound files (default: output/sounds)
--images-dir         Directory for image files (default: output/images)
--dictionary-url     Dictionary API URL (default: https://dictionary-api.eliaschen.dev)
```

### 3. Copy Media Files to Anki

After running the generator, copy the downloaded media files to Anki's media folder:

**macOS:**
```bash
cp output/sounds/* ~/Library/Application\ Support/Anki2/<YourProfile>/collection.media/
cp output/images/* ~/Library/Application\ Support/Anki2/<YourProfile>/collection.media/
```

**Windows:**
```bash
copy output\sounds\* %APPDATA%\Anki2\<YourProfile>\collection.media\
copy output\images\* %APPDATA%\Anki2\<YourProfile>\collection.media\
```

**Linux:**
```bash
cp output/sounds/* ~/.local/share/Anki2/<YourProfile>/collection.media/
cp output/images/* ~/.local/share/Anki2/<YourProfile>/collection.media/
```

Replace `<YourProfile>` with your Anki profile name (usually "User 1").

### 4. Import CSV to Anki

1. Open Anki
2. Click **File** → **Import**
3. Select your `output.csv` file
4. Configure import settings:
   - **Type**: Choose your note type (or create a new one with 9 fields)
   - **Deck**: Select target deck
   - **Field separator**: Comma
   - **Allow HTML in fields**: ✅ Checked
5. Map the CSV columns to your note fields:
   ```
   Column 1 (No)           → No
   Column 2 (Image)        → Image
   Column 3 (Vietnamese)   → Vietnamese
   Column 4 (Suggestion)   → Suggestion
   Column 5 (Keyword)      → Keyword
   Column 6 (Transcription)→ Transcription
   Column 7 (Explanation)  → Explanation
   Column 8 (Sound)        → Sound
   Column 9 (Example)      → Example
   ```
6. Click **Import**

## Output CSV Fields

| Field | Description | Example |
|-------|-------------|---------|
| No | Card number | 1 |
| Image | HTML image tag | `<img src="absorb_auto_tool.jpg">` |
| Vietnamese | Vietnamese translation | hút/thấm |
| Suggestion | Cloze hint | _ b _ _ r b |
| Keyword | English word | absorb |
| Transcription | IPA pronunciation | /əbˈsɔːrb/ |
| Explanation | Cloze definition | {{c1::absorb}} - to take something in |
| Sound | Anki sound syntax | [sound:absorb_auto_tool.mp3] |
| Example | Example sentences | - Plants absorb carbon dioxide.<br>- ... |

## Project Structure

```
├── src/
│   ├── main.py              # CLI entry point
│   ├── csv_handler.py       # CSV read/write
│   ├── dictionary_api.py    # Cambridge Dictionary API client
│   ├── sound_downloader.py  # Pronunciation downloader
│   ├── image_downloader.py  # Pexels image downloader
│   ├── suggestion.py        # Cloze hint generator
│   └── translator.py        # Google Translate fallback
├── output/
│   ├── sounds/              # Downloaded MP3 files
│   └── images/              # Downloaded images
├── cards_templates/         # Anki card templates (HTML/CSS)
├── input_sample.csv         # Example input file
└── requirements.txt
```

## License

MIT