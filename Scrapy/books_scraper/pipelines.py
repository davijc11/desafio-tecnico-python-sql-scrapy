import os
import requests
from urllib.parse import urlparse


class ImageDownloadPipeline:
    def process_item(self, item, spider):
        img_url = item.get('imagem_url')
        if img_url:
            filename = os.path.basename(urlparse(img_url).path)
            os.makedirs('imagens', exist_ok=True)
            filepath = os.path.join('imagens', filename)
            response = requests.get(img_url)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            item['imagem_local'] = filepath
        return item