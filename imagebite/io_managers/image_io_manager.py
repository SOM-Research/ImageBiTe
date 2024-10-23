from pathlib import Path
import requests


def save_or_download_image(test_id, prompt_id, instance_id, model, image_idx, image, is_url):
    full_path = get_full_path(test_id, prompt_id, instance_id, model, image_idx)
    p = Path(full_path['path'])
    p.mkdir(parents=True, exist_ok=True)
    with (p / full_path['filename']).open('wb') as handler:
        if (is_url):
            img_data = requests.get(image).content
            handler.write(img_data)
        else: # is bytes
            #image.save(p / filename, format="JPEG")
            handler.write(image)

def get_full_path(test_id, prompt_id, instance_id, model, image_idx):
    path = f'outputs/{test_id}/prompt_{prompt_id}/instance_{instance_id}/{model}'
    filename = f'image_{image_idx}.jpg'
    return {'path': path, 'filename': filename}