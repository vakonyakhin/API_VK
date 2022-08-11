import requests
from urllib.parse import urlparse, unquote
import os
from random import randint

from dotenv import load_dotenv


def get_comic(number):
    url = 'https://xkcd.com/info.0.json'
    responce = requests.get(url)
    responce.raise_for_status()
    max = responce.json()['num']

    number = randint(1, max)
    url = f'https://xkcd.com/{number}/info.0.json'
    responce = requests.get(url)
    responce.raise_for_status()
    image_url = responce.json()['img']
    text = responce.json()['alt']
    name = download_image(image_url)
    return text, name


def download_image(url):
    response = requests.get(url)
    response.raise_for_status()
    file_format = get_file_extention(url)
    name = f'xkcd{file_format}'
    with open(name, 'wb') as image:
        image.write(response.content)
    return name


def get_file_extention(url):
    url_parse = urlparse(url)
    file_name = unquote(os.path.split(url_parse.path)[1])
    file_extention = os.path.splitext(file_name)[1]
    return file_extention


def get_vk_groups(token):
    url = 'https://api.vk.com/method/groups.get'
    params = {
        'access_token': token,
        'filter': 'admin',
        'v': '5.131',

    }
    responce = requests.get(url, params=params)
    responce.raise_for_status()
    group_id = responce.json()['response']['items']
    return group_id


def get_upload_url(token, id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': token,
        'group_id': id,
        'v': '5.131',
    }
    responce = requests.get(url, params=params)
    responce.raise_for_status()
    upload_url = responce.json()['response']['upload_url']
    return upload_url


def upload_photo(upl_url, token, name):
    params = {
        'access_token': token,
        'v': '5.131',
            }
    with open(name, 'rb') as image:
        files = {
            'photo': image,
        }
        responce = requests.post(upl_url, params=params, files=files)
        responce.raise_for_status()
        server = responce.json()['server']
        photo = responce.json()['photo']
        hash_photo = responce.json()['hash']
        return server, photo, hash_photo


def save_photo(token, group_id, server, photo, photo_hash):

    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': token,
        'v': '5.131',
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': photo_hash,

    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    raw = response.json()
    photo_id = raw['response'][0]['id']
    owner_id = response.json()['response'][0]['owner_id']
    return photo_id, owner_id


def post_photo(token, group_id, photo_id, owner_id, text):
    attachment = f'photo{owner_id}_{photo_id}'
    url = 'https://api.vk.com/method/wall.post'
    params = {
         'access_token': token,
         'owner_id': f'-{group_id}',
         'message': text,
         'attachment': attachment,
    }
    responce = requests.post(url)
    responce.raise_for_status()


def delete_file(name):
    os.remove(name)


def main():
    load_dotenv()
    number = randint(0, 600)
    token = os.getenv('ACCESS_TOKEN')
    group_id = os.getenv('GROUP_ID')
    comment, name = get_comic(number)
    upload_url = get_upload_url(token, group_id)
    server, photo, photo_hash = upload_photo(upload_url, token, name)
    photo_id, owner_id = save_photo(token, group_id, server, photo, photo_hash)
    post_photo(token, group_id, photo_id, owner_id, comment)
    delete_file(name)


if __name__ == '__main__':
    main()
