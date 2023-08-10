import os
import time
import threading
from collections import defaultdict
import yaml
import requests

# Load Configuration from YAML
with open("configuration.yaml", 'r') as file:
    config = yaml.safe_load(file)

DOWNLOAD_DIR = config['gyazo']['download_directory']
MAX_THREADS = config['gyazo']['max_threads']
IMAGES_PER_REQUEST = config['gyazo']['images_per_request']
DELAY_BETWEEN_REQUESTS = config['gyazo']['delay_between_requests']
SESSION_COOKIE = config['gyazo']['session_cookie']

session = requests.Session()

images = []
page = 1

while True:
    print(f'[{page}] Fetching images...', end='', flush=True)
    resp = session.get(
        f'https://gyazo.com/api/images?page={page}&per_page={IMAGES_PER_REQUEST}', 
        cookies={'Gyazo_session': SESSION_COOKIE}
    )
    
    if not resp.json():
        break

    images.extend(resp.json())
    page += 1
    time.sleep(DELAY_BETWEEN_REQUESTS)
    print(' done!')

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

file_types = defaultdict(int)
lock = threading.Lock()

def download_image(image):
    global file_types

    url = image['url']
    ext = url.split('.')[-1]

    filename = f'{DOWNLOAD_DIR}/{image["image_id"]}.{ext}'

    if not os.path.exists(filename):
        time.sleep(DELAY_BETWEEN_REQUESTS)
        resp = session.get(url)

        with open(filename, 'wb') as f:
            f.write(resp.content)

        with lock:
            file_types[ext] += 1
            print(f"[Downloaded] {filename}")

threads = []

for image in images:
    while threading.active_count() >= MAX_THREADS:
        time.sleep(0.1)

    thread = threading.Thread(target=download_image, args=[image])
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print('Download complete!')
print(f'Total: {sum(file_types.values())}')
for k, v in file_types.items():
    print(f'{k}: {v}')