# CSV Column Translator

A Python script that translates specified columns in a CSV file from one language to another using either Google Translate or OpenAI's GPT models.

## Features

- Translates one or multiple columns in a CSV file
- Two translation engines:
  - **Google Translate**: Fast, free, good for general text
  - **OpenAI GPT-4o-mini**: Higher quality, context-aware, specialized for e-commerce content
- Specialized prompts for product titles and descriptions
- Progress bar for tracking translation status
- Error handling for failed translations
- Supports all languages available in Google Translate and OpenAI

## Requirements

Install dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas deep-translator tqdm openai python-dotenv
```

## Setup

### For OpenAI Translation

Create a `.env` file in the same directory as the script:

```
OPENAI_KEY=your_openai_api_key_here
```

You can get an API key from [OpenAI Platform](https://platform.openai.com/api-keys).

## Usage

### Basic Command

```bash
python script.py input.csv output.csv --src en --tgt ro
```

### Parameters

- `input` - Path to the input CSV file
- `output` - Path to save the translated CSV file
- `--src` - Source language code (e.g., `en` for English)
- `--tgt` - Target language code (e.g., `ro` for Romanian)

### Interactive Prompts

When you run the script, you'll be asked:

1. **Which columns to translate:**
   ```
   What column to translate?
   ```
   Enter column indices (0-based) separated by spaces. Examples:
   - `0` - translates only the first column
   - `0 2 3` - translates columns 0, 2, and 3

2. **Which translation engine to use:**
   ```
   What to use?
    1. GoogleTranslate
    2. OpenAI
   ```
   Enter `1` for Google Translate or `2` for OpenAI.

3. **For OpenAI only - content type for each column:**
   ```
   Content type for column 'Title' [title/description/text]:
   ```
   - `title` - Optimized for product titles (concise, SEO-friendly)
   - `description` - Optimized for product descriptions (maintains formatting and tone)
   - `text` - General text translation

## Examples

### Example 1: Google Translate
```bash
python script.py input_text.csv output.csv --src de --tgt en
# When prompted:
# What column to translate? 2 3
# What to use? 1
```

### Example 2: OpenAI for E-commerce
```bash
python script.py products.csv translated_products.csv --src en --tgt ro
# When prompted:
# What column to translate? 1 2
# What to use? 2
# Content type for column 'Title' [title/description/text]: title
# Content type for column 'Description' [title/description/text]: description
```

## Language Codes

Common language codes:
- `en` - English
- `fr` - French
- `de` - German
- `ro` - Romanian

For Google Translate, see the [full list of supported languages](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages).

## How It Works

1. Reads the CSV file into a pandas DataFrame
2. Prompts user for column selection and translation method
3. For each specified column:
   - Converts all values to strings (handles NaN as empty strings)
   - Translates text using selected engine
   - Updates the DataFrame with translations
4. Saves the translated DataFrame to the output CSV file
5. Displays completion message

## Error Handling

- If translation fails for a row, an empty string is inserted
- Error messages are printed to console
- Processing continues with remaining rows
- Partial results are saved to the output file

## Notes

- For OpenAI translation, you need a valid API key and will incur usage charges
- The script saves progress incrementally when using OpenAI (after each column)
- Brand names, model numbers, and technical specifications are preserved when using OpenAI's specialized prompts