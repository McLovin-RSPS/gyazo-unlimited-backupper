import base64
import concurrent.futures
import filedate
import json
import os
import requests
import streamlit as st

session = requests.Session()

# Define function to fetch and download images
def fetch_and_download_images(cookie, search_term):
    images = set()
    page = 1
    st.write(f"Fetching images using search term: {search_term}...")

    with st.spinner("Fetching images..."):
        while True:
            try:
                request = session.get(
                    f"https://gyazo.com/api/internal/images?page={page}&per=100",
                    cookies={"Gyazo_session": cookie}
                )
            except Exception as e:
                st.error(f"An error occurred while fetching images: {e}")
                return

            if request.text == "[]":
                break

            images.update(request.json())

            page += 1

    media_path = "media"
    search_term_path = os.path.join(media_path, search_term)
    os.makedirs(search_term_path, exist_ok=True)

    metadata_dict = {}
    log_dict = {}

    total_images = len(images)
    current_image = 1
    prog_bar = st.empty()

    def download_image(image):
        nonlocal current_image

        metadata = image['metadata']

        # Check if search term is in metadata
        if search_term.lower() in str(metadata).lower():
            jwt = image['alias_id']
            url = image['non_cropped_thumb']['url']

            payload = json.loads(base64.b64decode(jwt.split('.')[1] + "=="))
            id = payload['img']
            ext = os.path.splitext(url)[1]

            directory = os.path.join(search_term_path, ext)
            os.makedirs(directory, exist_ok=True)

            if "app" in metadata:
                filename = f"{metadata['app']}{id}.{ext}"
            elif "title" in metadata:
                filename = f"{metadata['title']}{id}.{ext}"
            else:
                filename = f"{id}.{ext}"

            filepath = os.path.join(directory, filename)

            if not os.path.exists(filepath):
                try:
                    request = session.get(f"https://thumb.gyazo.com/thumb/8192/{id}.{ext}")
                except Exception as e:
                    st.error(f"An error occurred while downloading image: {e}")
                    # Do not return, continue with the next image

                with open(filepath, "wb") as file:
                    file.write(request.content)

                timestamp = image['created_at']
                filedate.File(filepath).set(
                    created=timestamp,
                    modified=timestamp
                )

                metadata_dict[filepath] = metadata
                log_dict[filepath] = f"Downloaded: {filename}"

            current_image += 1
            prog_bar.progress(current_image / total_images)

    # Use ThreadPoolExecutor with 10 workers for parallel downloads
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_image, image) for image in images]

        for future in concurrent.futures.as_completed(futures):
            pass

    # Save metadata to a single text file with utf-8 encoding
    with open("metadata.txt", "w", encoding="utf-8") as f:
        json.dump(metadata_dict, f, ensure_ascii=False)

    # Save log data to log.txt
    with open("log.txt", "w", encoding="utf-8") as f:
        json.dump(log_dict, f, ensure_ascii=False)

    st.write(f"Downloaded {current_image} images based on the search term.")

# Streamlit UI
st.title("Gyazo Media Downloader")
st.write("Download media from Gyazo based on metadata search.")

cookie = st.text_input("Enter Gyazo session cookie:")
search_term = st.text_input("Enter a search term to filter media by metadata:")
if st.button("Start Download"):
    fetch_and_download_images(cookie, search_term)
