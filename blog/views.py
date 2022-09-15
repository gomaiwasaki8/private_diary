from django.views import generic
from .forms import BlogInquiryForm

class BlogIndexView(generic.TemplateView):
    template_name = "blogindex.html"

class BlogInquiryView(generic.FormView):
    template_name = "bloginquiry.html"
    form_class = BlogInquiryForm

