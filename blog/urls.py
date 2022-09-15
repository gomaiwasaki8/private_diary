from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    # ルーティングの仕組みに名前を付けているname。間違えるとエラー。
    path('', views.BlogIndexView.as_view(), name = "blogindex"),
    path('bloginquiry/', views.BlogInquiryView.as_view(), name = "bloginquiry"),

]