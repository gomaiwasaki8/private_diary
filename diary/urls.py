from django.urls import path
from . import views
app_name = 'diary'
urlpatterns = [
    # ルーティングの仕組みに名前を付けているname。間違えるとエラー。
    path('', views.IndexView.as_view(), name = "index"),
    path('inquiry/', views.InquiryView.as_view(), name = "inquiry"), # お問い合わせ
    path('diary-list/', views.DiaryListView.as_view(), name = 'diary_list'), # 日記の一覧
    path('diary-detail/<int:pk>/', views.DiaryDetailView.as_view(), name = 'diary_detail'), # 日記詳細表示
    path('diary-create/', views.DiaryCreateView.as_view(), name = 'diary_create'), # 日記作成機能
]