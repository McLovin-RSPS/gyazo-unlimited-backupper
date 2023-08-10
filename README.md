# gyazo-unlimited-backupper


Download your entire capture history from Gyazo using your session cookie with this Python script. Built to handle large volumes of images and optimized for performance using threading.

## Prerequisites

- Python 3 (this script is not tested with Python 2)
  
## Configuration Setup

1. Ensure you have your Gyazo session cookie. This can usually be found in your browser's developer console when logged into Gyazo.
2. Update the `configuration.yaml` file with the correct parameters:
    - `session_cookie`: Your Gyazo session cookie.
    - `download_directory`: The directory where images will be saved.
    - `images_per_request`: Number of images fetched per API request.
    - `delay_between_requests`: Delay (in seconds) between consecutive requests to avoid hitting rate limits.
    - `max_threads`: Maximum number of threads for concurrent downloads.

## Installing Dependencies

1. Use pip to install the necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Script

To run the downloader:

```bash
python main.py
```

Images will be downloaded to the specified directory in the `configuration.yaml` file (default: `./downloads/`).

## Output

The script provides console output for:

- Current progress in terms of fetched images and pages.
- Download status for each image.
- Total number of images downloaded.
- Breakdown of images by file type (e.g., PNG, GIF, MP4, etc.).
