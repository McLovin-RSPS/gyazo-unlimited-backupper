# gyazo-unlimited-backupper (Gyazo Media Downloader with Streamlit UI)




This Python script provides a simple Streamlit-based UI to download media from Gyazo based on a search term in their metadata.

## Features

- User-friendly UI with Streamlit.
- Filter and download media based on metadata search.
- Saves metadata for each downloaded image to a consolidated file (`metadata.txt`).
- Maintains an operation log in `log.txt`.
- Organizes different media types in separate directories within a `media` directory.

## Installation

1. Clone the repository:

```
git clone https://github.com/McLovin-RSPS/gyazo-unlimited-backupper
```

2. Navigate to the project directory:

```
cd gyazo-unlimited-backupper
```

3. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

1. Run the script:

```
streamlit run app.py
```

2. Open the provided link in your browser.
3. Enter the Gyazo session cookie and desired search term.
4. Click "Start Download" to begin the download process.

## Note

Make sure you have a valid Gyazo session cookie to use the script.