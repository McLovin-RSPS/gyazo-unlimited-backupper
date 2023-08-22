import base64
import concurrent.futures
import filedate
import json
import os
import requests
import streamlit as st
import time

session = requests.Session()

# Define function to fetch and download images
def fetch_and_download_images(cookie, search_term):
    images = []
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

            images += request.json()

            page += 1

    media_path = "media"
    if not os.path.exists(media_path):
        os.makedirs(media_path)

    metadata_list = []
    log_data = []

    total_images = len(images)
    current_image = 1
    prog_bar = st.progress(0)

    def download_image(image):
        nonlocal current_image

        metadata = image['metadata']

        # Check if search term is in metadata
        if search_term.lower() in str(metadata).lower():
            jwt = image['alias_id']
            url = image['non_cropped_thumb']['url']

            payload = json.loads(base64.b64decode(jwt.split('.')[1] + "=="))
            id = payload['img']
            ext = url[-7:-4]

            directory = media_path + "/" + ext
            if not os.path.exists(directory):
                os.makedirs(directory)

            if "app" in metadata:
                filename = f"{directory}/{metadata['app']}{id}.{ext}"
            elif "title" in metadata:
                filename = f"{directory}/{metadata['title']}{id}.{ext}"
            else:
                filename = f"{directory}/{id}.{ext}"

            if not os.path.exists(filename):
                try:
                    request = session.get(f"https://thumb.gyazo.com/thumb/8192/{id}.{ext}")
                except Exception as e:
                    st.error(f"An error occurred while downloading image: {e}")
                    return

                with open(filename, "wb") as file:
                    file.write(request.content)

                timestamp = image['created_at']
                filedate.File(filename).set(
                    created=timestamp,
                    modified=timestamp
                )

                metadata_list.append(metadata)
                log_data.append(f"Downloaded: {filename}")

            current_image += 1
            prog_bar.update(current_image / total_images)
            
            # Introduce delay between successive API requests to respect rate limits
            time.sleep(0.5)

    # Use ThreadPoolExecutor for parallel downloads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, images)

    # Save metadata to a single text file
    with open("metadata.txt", "w") as f:
        for item in metadata_list:
            f.write("%s\n" % item)

    # Save log data to log.txt
    with open("log.txt", "w") as f:
        for log_item in log_data:
            f.write("%s\n" % log_item)

    st.write(f"Downloaded {current_image} images based on the search term.")

# Streamlit UI
st.title("Gyazo Media Downloader")
st.write("Download media from Gyazo based on metadata search.")

cookie = st.text_input("Enter Gyazo session cookie:")
search_term = st.text_input("Enter a search term to filter media by metadata:")
if st.button("Start Download"):
    fetch_and_download_images(cookie, search_term)