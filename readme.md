###updated
  
Можно использовать проект как отдельный (standalone), так отдельно батарейку "apiapp"  
Для этого в настройки надо добавить пути до файлов, и сам app
```
# settings.py
INSTALLED_APPS = [
    ...
    'apiapp',
    ...
]

CERTIFICATE_FILE = "/path/to/file/some.srt" # ex: './files/client03test.crt'
KEY_FILE = "/path/to/file/some.key" # ex: './files/client03test.key'
```
Так же необходимо добавить в `urls.py` приложения url
```
# url.py
path('api/', include('apiapp.urls')),
```

При желании можно добавить в settings настройки логгирования или обновить существующие.  
Перенеся файл `logger_settings.py.tmp` в `testauth/logger_settings.py` и добавив
```
# settings.py
from .logger_settings import LOGGING
```
Или просто весь словарь из `logger_settings.py.tmp`

Добавлены шаблоны для вывода и отдельный класс для запроса `api_request.BaseRequest`.  
При создании экземпляра BaseRequest принимает два параметра  
url - адрес апи  
logging - default True - использовать ли логгирование

Класс имеет публичный метод `make_request`, с параметрами
method - метод api  
rid: возможный id запроса  
params: опциональный параметры  
Возвращает текст запроса