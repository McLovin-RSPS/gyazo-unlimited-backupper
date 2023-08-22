import base64
import filedate
import json
import os
import requests
import streamlit as st

session = requests.Session()

# Define function to fetch and download images
def fetch_and_download_images(cookie, search_term):
    images = []
    page = 1
    st.write(f"Fetching images using search term: {search_term}...")
    
    while True:
        request = session.get(
            f"https://gyazo.com/api/internal/images?page={page}&per=100",
            cookies={"Gyazo_session": cookie}
        )

        if request.text == "[]":
            break

        images += request.json()

        page += 1

    media_path = "media"
    if not os.path.exists(media_path):
        os.makedirs(media_path)

    metadata_list = []
    log_data = []

    count = 1
    for image in images:
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
                request = session.get(f"https://thumb.gyazo.com/thumb/8192/{id}.{ext}")

                with open(filename, "wb") as file:
                    file.write(request.content)

                timestamp = image['created_at']
                filedate.File(filename).set(
                    created=timestamp,
                    modified=timestamp
                )

                metadata_list.append(metadata)
                log_data.append(f"Downloaded: {filename}")

            count += 1

    # Save metadata to a single text file
    with open("metadata.txt", "w") as f:
        for item in metadata_list:
            f.write("%s\n" % item)

    # Save log data to log.txt
    with open("log.txt", "w") as f:
        for log_item in log_data:
            f.write("%s\n" % log_item)

    st.write(f"Downloaded {count} images based on the search term.")

# Streamlit UI
st.title("Gyazo Media Downloader")
st.write("Download media from Gyazo based on metadata search.")

cookie = st.text_input("Enter Gyazo session cookie:")
search_term = st.text_input("Enter a search term to filter media by metadata:")
if st.button("Start Download"):
    fetch_and_download_images(cookie, search_term)
