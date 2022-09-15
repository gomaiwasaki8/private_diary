from django.contrib import admin
# 同じディレクトリのmodelsファイルのDiaryっていうのをインポート
from . models import Diary

admin.site.register(Diary)