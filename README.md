# Gyazo Unlimited Backupper: Gyazo Media Downloader & Backup Tool with Streamlit UI

Looking for a reliable tool to download and backup your Gyazo captures? Gyazo Unlimited Backupper is a Python-based solution that offers a user-friendly Streamlit UI, allowing you to effortlessly download media from Gyazo based on metadata search terms.

## Key Features

- **Gyazo Captures Downloader**: Easily download media from Gyazo with a simple search.
- **Backup Tool**: Save and organize your Gyazo captures for safekeeping.
- **User-friendly Streamlit UI**: No technical expertise required.
- **Metadata Management**: Saves metadata for each downloaded image to a consolidated file (`metadata.txt`).
- **Logging**: Maintains an operation log in `log.txt` for transparency.
- **Organized Storage**: Different media types are stored in separate directories within a `media` directory.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/McLovin-RSPS/gyazo-unlimited-backupper
   ```

2. Navigate to the project directory:
   ```bash
   cd gyazo-unlimited-backupper
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   streamlit run app.py
   ```

2. Open the provided link in your browser.
3. Enter the Gyazo session cookie and desired search term.
4. Click "Start Download" to initiate the download and backup process.

## Important Notes

- Ensure you have a valid Gyazo session cookie to utilize the script.
- The script creates a `media` directory to house the downloaded media.
- Metadata for each downloaded image is stored in `metadata.txt`.
- Download progress and any encountered errors are logged in `log.txt`.
