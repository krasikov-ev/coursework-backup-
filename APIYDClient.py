from dependencies import requests
from dependencies import datetime


class APIYDClient:

    YD_Base_Url = 'https://cloud-api.yandex.net'

    def __init__(self, token):
        self.token = token

    def create_folder(self, folder_name):
        """Создаёт на ЯД папку с именем {folder_name}"""
        YD_create_folder_URL = f'{self.YD_Base_Url}/v1/disk/resources'
        params = {'path': folder_name}
        headers = {"Authorization": f'OAuth {self.token}'}
        response = requests.put(YD_create_folder_URL, params=params, headers=headers)
        if response.status_code == 201:                       
            print (f'Папка {folder_name} создана {datetime.datetime.now()}')
        elif response.status_code == 409:
            print (f'Папка {folder_name} уже была создана ранее')
        else:
            print(f'Папка не создана. Код ошибки {response.status_code}')
            print(response.text)

    def resource_upload(self, file_name, file_url, folder_name):
        """Создаёт в папке {folder_name} на ЯД файл с именем {file_name}.png из картинки по адресу {file_url}."""       
        response_pict = requests.get(file_url)       
        YD_folder_for_upload_Url = f'{self.YD_Base_Url}/v1/disk/resources/upload'
        params = {'path': f'{folder_name}/{file_name}.png'}
        headers = {"Authorization": f'OAuth {self.token}'}
        response = requests.get(YD_folder_for_upload_Url, params=params, headers=headers)
        if response.status_code == 200:
            url_for_upload = response.json()["href"]            
        else:
            print(f'Ошибка {response.status_code} при получении ссылки для создания файла')        
        response_put = requests.put(url_for_upload, data=response_pict.content)
        if  response_put.status_code != 201:
            print(f'Ошибка {response_put.status_code} при создании файла')

    
        
        


