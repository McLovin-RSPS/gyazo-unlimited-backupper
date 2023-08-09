import os
import requests
from gyazo import Api
from yaml import safe_load

def download_images(settings):
    if 'token' not in settings or not settings['token']:
        raise ValueError("Need to specify token in ./client.yml")

    client = Api(access_token=settings['token'])
    images_dir = "./images"
    os.makedirs(images_dir, exist_ok=True)

    for i in range(1, 10000):
        images = client.get_image_list(per_page=100, page=i)
        if not images:
            break

        for image in images:
            if not image.url:
                continue
            r = requests.get(image.url, stream=True)
            if r.status_code == 200:
                img_path = os.path.join(images_dir, f"{image.image_id}.png")
                if os.path.exists(img_path):
                    print(f"Skipping image_id {image.image_id} as it already exists")
                    continue
                with open(img_path, "wb") as imgfile:
                    print(f"Writing to file {image.image_id}.png")
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            imgfile.write(chunk)
            else:
                print(f"Failed to download image: {image.url}")

def load_settings(file_path="./client.yml"):
    with open(file_path, "r") as f:
        return safe_load(f)

if __name__ == '__main__':
    settings = load_settings()
    download_images(settings)
