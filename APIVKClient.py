from dependencies import requests
from dependencies import json
from dependencies import time


class APIVKClient:

    VK_Base_URL = 'https://api.vk.com/method'

    def __init__(self, token):
        self.token = token

    def get_common_params(self):
        return {
            "access_token": self.token,
            "v": '5.199',           
        }

    def photos_get(self, owner_id, album_id = 'profile'):
        params = self.get_common_params()
        params.update({"owner_id": owner_id, "extended": 1, "album_id": album_id})
        response = requests.get(f'{self.VK_Base_URL}/photos.get', params=params)
        return response
        
    def photos_write(self, owner_id, album_id = 'profile'):
        """Записывает и возвращает необходимую далее информацию о всех фото альбома в photos_dict"""
        data = self.photos_get(owner_id, album_id)       
        photos_dict = {}
        # size_value_dict - порядок сортировки для типа фотографий
        size_value_dict = {'w': 1, 'z': 2, 'y': 3, 'x': 4, 'r': 5, 'q': 6, 'p': 7, 'm': 8, 'o': 9,'s': 10}
        for photo in data.json()["response"]["items"]:
            photos_dict[photo["id"]] = {
                "likes_qty": photo["likes"]["count"],
                "date":  time.strftime("%Y-%m-%d--%H-%M-%S", time.gmtime(photo["date"])),
                # "url": sorted(photo["sizes"], key = lambda x: x["height"]*x["width"], reverse=True)[0]["url"],
                # "size": sorted(photo["sizes"], key = lambda x: x["height"]*x["width"], reverse=True)[0]["type"]
                "url": sorted(photo["sizes"], key = lambda x: size_value_dict[x["type"]])[0]["url"],
                "size": sorted(photo["sizes"], key = lambda x: size_value_dict[x["type"]])[0]["type"]
                }        
        return photos_dict        

    def get_albums (self, owner_id):
        """Получает список альбомов пользователя"""
        params = self.get_common_params()
        params.update({"owner_id": owner_id})
        response = requests.get(f'{self.VK_Base_URL}/photos.getAlbums', params=params)        
        albums_dict = {}        
        if response.json()["response"]["count"] > 0:
            for album in response.json()["response"]["items"]:
                albums_dict[album["id"]] = {
                    "title": album["title"],
                    "size": album["size"]
                    }
        else:
            print ('Нет дополнительных альбомов')
            return 0       
        return albums_dict
       
        
        


if __name__ == '__main__':
   
    
    vkklient.photos_write('')
    # vkklient.photos_get('')
    # vkklient.get_albums ('')
    # print(vkklient.photos_write('', ))


