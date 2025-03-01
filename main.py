from dependencies import json
from dependencies import configparser
from dependencies import tqdm
from dependencies import logging
from dependencies import NoReturn
from APIVKClient import APIVKClient
from APIYDClient import APIYDClient


config = configparser.ConfigParser()
config.read('settings.ini')
VKtoken = config['Tokens']['VKtoken']
YDtoken = config['Tokens']['YDtoken']

vkklient = APIVKClient(VKtoken)
ydklient = APIYDClient(YDtoken)

def save_VKphotos_in_YD(user_VK_id: int, PYDtoken: str, photos_quantity: int = 5, album_id: str = 'profile', folder_name: str = '', rewrite_results: str = 'w') -> NoReturn:
    """
    Функция получает список фотографий с профиля {user_VK_id} ВК.     
    Из полученного списка фотографии в количестве {photos_quantity} сохраняется в папку с именем {album_id} на ЯД.
    Для имени фотографии используется количество лайков и, в случае их дублирования, дата загрузки.
    Информация о сохранённых фотографиях записывается в results.json.

    Параметры:
        user_VK_id (int): ИД пользователя ВК.
        PYDtoken (str): Токен для VK API.
        photos_quantity (int): Количество фотографий для загрузки (по умолчанию 5).
        album_id (str): Имя альюома для загрузки. По умолчанию 'profile'. Можно использовать 'wall' или ид пользовательского альбома.
        folder_name (str): Имя папки для загрузки фото на Яндекс Диске. По умолчанию равно названию альбома ВК.
        rewrite_results (str): Режим записи файла results.json. По умолчанию 'w'. При вызове из функции save_other_VKphotos_in_YD - 'a'.
    """
    if not folder_name:
        folder_name = album_id
    # Получаем список фотографий пользователя:   
    photos_dict = vkklient.photos_write(user_VK_id, album_id)
    # Проверяем количество фотографий в нём:
    if len(photos_dict) == 0:
        print('Нет данных для заполнения')
        return  None
    print(f'В альбоме {album_id} {len(photos_dict)} фотографй')
    if len(photos_dict) < photos_quantity:
        photos_quantity = len(photos_dict)    
    # Созжаём на ЯД папку {folder_name}:
    ydklient.create_folder(folder_name)
    # Сохраняем {photos_quantity} фотографий в папку {folder_name} и заполняем result_list для выврода в result.json :
    result_list = []
    photo_likes_qty = []
    for photo_id in tqdm(list(photos_dict.keys())[:photos_quantity], desc = 'the file upload process', colour = 'CYAN', position=0, leave=True):
        # Определяем название файла (кол-во лайков или кол-во лайков+дата загрузки)
        if photos_dict[photo_id]["likes_qty"] in photo_likes_qty:
            file_name = f'{photos_dict[photo_id]["likes_qty"]}-{photos_dict[photo_id]["date"]}'
        else:
            file_name = photos_dict[photo_id]["likes_qty"]
            photo_likes_qty.append(photos_dict[photo_id]["likes_qty"])       
        # Загружаем файл на диск и заполняем список для заполнения results.json
        result_list.append({"file_name": f'{file_name }.png',"size":photos_dict[photo_id]["size"]})
        ydklient.resource_upload(file_name, photos_dict[photo_id]["url"], folder_name)
    # Записываеи результат в results.json:   
    with open("results.json", rewrite_results, encoding='utf-8') as f:
        json.dump(result_list, f, ensure_ascii=False, indent=4)
        print('Файлы записаны в results.json')

def save_other_VKphotos_in_YD(user_VK_id: int, PYDtoken: str, photos_quantity: int = 5, all_albums: bool = False) -> NoReturn:
    """
    Функция получает список всех альбов пользователей и вызывает save_VKphotos_in_YD для каждого альбома. 
    В файл results.json записываются данные о всех сохранённых фото. 

    Параметры:
        user_VK_id (int): ИД пользователя ВК.
        PYDtoken (str): Токен для VK API.
        photos_quantity (int): Количество фотографий для загрузки для каждого альбома(по умолчанию 5).
        all_albums (bool): Обрабатывать служебные альбомы (profile и wall). По умолчанию False - не обрабатывать.
    """
    with open("results.json", 'w', encoding='utf-8') as f:
        pass
    albums_dict = vkklient.get_albums(user_VK_id)
    service_albums = {'wall': {'title': 'wall'}, 'profile': {'title': 'profile'}}
    if all_albums and albums_dict:
        albums_dict.update(service_albums)
    if all_albums and not albums_dict:
         albums_dict = service_albums
    if albums_dict:
        for album in albums_dict:        
            save_VKphotos_in_YD(user_VK_id, PYDtoken, photos_quantity, album, albums_dict[album]['title'], 'a')
        print (f'Создано {len(albums_dict)} папок')
    else:
        print ('Нет файлов для загрузки')

   


# save_VKphotos_in_YD(__, YDtoken, 5, 'profile', 'some_folder')
# save_other_VKphotos_in_YD(__, YDtoken, 3 )
 