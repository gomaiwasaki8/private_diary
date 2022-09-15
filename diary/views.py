from django.views import generic
import logging
from django.urls import reverse_lazy
from .forms import InquiryForm
logger = logging.getLogger(__name__)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import Diary

# TemplateViewを継承しているらしい
class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    # 入力されたフォームを使う設定。親のクラスで定義されている変数名なので変更するな。
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')
    # success_urlはdiary:inquiry（urls.pyで定義されているnameを参照）の画面に遷移

    # 親のクラス（generic.FormView）で定義されているメソッド（form_valid）を継承して子側で内容を書き換えるオーバーライド。
    # form_validメソッドは、フォームのバリデーションという名の通り、入力内容に問題が無かったら実行されるメソッド。
    def form_valid(self, form):
        form.send_email() # forms.pyで定義されているsend_wmailメソッドを実行する記述
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

# 日記一覧表示。LoginRequiredMixinはログインしているユーザじゃないと見れないって設定
class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name = 'diary_list.html'

    # メソッドのオーバーライド。filterとは抽出。自分が登録した日記を自分だけが見れるという前提だからこうなっている。order_byは表示する順番。
    def get_queryset(self):
        diaries = Diary.objects.filter(user = self.request.user).order_by('-created_at')
        return diaries