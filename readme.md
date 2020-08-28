Можно использовать проект как отдельный (standalone), так отдельно батарейку "apiapp"  
Для этого в файл  надо добавить пути до файлов`
```
# settings.py
CERTIFICATE_FILE = "/path/to/file/some.srt" # ex: './files/client03test.crt'
KEY_FILE = "/path/to/file/some.key" # ex: './files/client03test.key'
```
Так же добавить в urls.py приложения url
```
# url.py
path('api/', include('apiapp.urls')),
```
