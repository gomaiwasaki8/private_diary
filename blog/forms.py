from django import forms

class BlogInquiryForm(forms.Form):
    name = forms.CharField(label = 'おなまえ', max_length = 30)
    email = forms.EmailField(label = 'めーるあどれす')
    title = forms.CharField(label = 'たいとる', max_length = 30)
    message = forms.CharField(label = 'めっせーじ', widget = forms.Textarea)

    # 無くても動くが、placeholderは初期値を設定している。入力欄に薄い字が表示される。classはデザインの設定
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'


