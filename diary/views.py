from django.views import generic
import logging
from django.urls import reverse_lazy
from .forms import InquiryForm, DiaryCreateForm
logger = logging.getLogger(__name__)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . models import Diary
from django.shortcuts import get_object_or_404


class OnlyYouMixin(UserPassesTestMixin):  # 日記作成者のみ閲覧できる機能
    raise_exception = True

    def test_func(self):
        # URLに埋め込まれた主キーから日記データを1件取得。取得できなかった場合は404エラー
        diary = get_object_or_404(Diary, pk = self.kwargs['pk'])
        # ログインユーザと日記の作成ユーザを比較し、異なればraise_exeptionの設定に従う
        return self.request.user == diary.user

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
    paginate_by = 2 # 数字は多分表示する数

    # メソッドのオーバーライド。filterとは抽出。自分が登録した日記を自分だけが見れるという前提だからこうなっている。order_byは表示する順番。
    def get_queryset(self):
        diaries = Diary.objects.filter(user = self.request.user).order_by('-created_at')
        return diaries

# 日記詳細表示のクラス
class DiaryDetailView(LoginRequiredMixin, OnlyYouMixin, generic.DetailView):
    # 詳細画面を表示するにはモデル（データベースと連携させるモデル）が必要
    model = Diary
    template_name = 'diary_detail.html'

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form): # 登録が成功した時の処理。formはユーザが入力したのが入っている
        diary = form.save(commit = False) # 日記をセーブ（登録）する。commit=Falseはまだすべての情報が入っていないからコミットしないって意味
        diary.user = self.request.user # ユーザ名を入れている（ユーザが入力しないでいいようにこっちでユーザ名をセットする）
        diary.save()
        messages.success(self.request, "日記を作成しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, OnlyYouMixin, generic.UpdateView): # UpdateViewクラスを継承している
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm # 日記作成機能にも使ったフォームを使いまわしてる。

    def get_success_url(self): # オーバーライド
        return reverse_lazy('diary:diary_detail', kwargs = {'pk': self.kwargs['pk']})

    def form_valid(self, form): # 更新が成功した時の処理。formはユーザが入力したのが入っている。オーバーライド。
        messages.success(self.request, "日記を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form): # オーバーライド
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin, OnlyYouMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary_delete.html'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)
