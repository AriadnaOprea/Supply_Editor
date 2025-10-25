# CSV Column Translator

A Python script that translates specified columns in a CSV file from one language to another using Google Translate.

## Features

- Translates one or multiple columns in a CSV file
- Processes large files in chunks to manage memory efficiently
- Progress bar for tracking translation status
- Error handling for failed translations
- Supports all languages available in Google Translate

## Requirements

Install dependencies using the provided requirements file:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install pandas deep-translator tqdm
```

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

### Interactive Column Selection

When you run the script, it will prompt you to specify which columns to translate:

```
What column need to be translated?
```

Enter the column indices (0-based) separated by spaces. For example:
- `0` - translates only the first column
- `0 2 3` - translates columns 0, 2, and 3

## Example

An example input file `input_text.csv` is included with German text. It contains title and description columns at indices 2 and 3.

```bash
python script.py input_text.csv output.csv --src de --tgt en
# When prompted: 2 3
# This translates the title and description columns from German to English
```

## Language Codes

Common language codes:
- `en` - English
- `fr` - French
- `de` - German
- `ro` - Romanian

[Full list of languages](https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages)

## How It Works

1. Reads the CSV file in chunks (100 rows at a time by default)
2. For each specified column, translates all text values
3. Handles missing values (NaN) by converting them to empty strings
4. Saves the translated data to a new CSV file
5. Displays the final result

## Error Handling

If a translation fails for any text, the script:
- Prints an error message
- Inserts an empty string for that cell
- Continues processing the remaining data
