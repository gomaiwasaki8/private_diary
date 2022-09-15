# 開発環境用

# settings_common（本番＆開発共通ファイル）の内容を取り込んでいる
from .settings_common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-44dprt8-*#c(@!@y20%@()i6n_cx5v9k*bhs4xk4j7jsm5c-_t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # デバックの表示がTrueって意味

ALLOWED_HOSTS = []

# ロギング設定
LOGGING = {
    'version':1, # 固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # diaryアプリケーションが利用するロガー
        'diary': {
            'handlers':['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console' :{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev',
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

# メール処理で使うバックエンドを定義（開発時のメール配信先設定）つまり入力されたものがコンソールに表示される
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# メディアファイルの配置場所を指定
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # BASE_DIRはsettings_commonで定義されている