from django.contrib import admin
from django.urls import path, include
# 開発サーバでメディアファイルを配信するために利用する
from django.contrib.staticfiles.urls import static
from . import settings_common, settings_dev
# 同じフォルダ内の事を指すときは.ドット。

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('diary.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('allauth.urls')), # アカウントのアプリケーションへ
]

# 開発サーバでメディアを配信できるようにする設定
urlpatterns += static(settings_common.MEDIA_URL, document_root = settings_dev.MEDIA_ROOT)
