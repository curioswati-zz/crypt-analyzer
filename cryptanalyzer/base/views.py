from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic

from .forms import UploadFileForm, SelectAlgorithmForm


class IndexView(generic.TemplateView):
    template_name = "index.html"


class ContactView(generic.TemplateView):
    template_name = "index.html"


class EncryptionData(generic.FormView):
    form_class = UploadFileForm
    success_url = "base:select_algorithm"
    template_name = "encryption_data.html"

    def form_valid(self, form):
        data = []
        for field in form.fields:
            f = form[field].value()
            data.append(f.read())

        return HttpResponseRedirect(reverse_lazy(self.success_url))


class EncryptionKey(generic.TemplateView):
    template_name = "encryption_key.html"


class DecryptionData(generic.FormView):
    form_class = UploadFileForm
    success_url = "base:select_algorithm"
    template_name = "decryption_data.html"

    def form_valid(self, form):
        data = []
        for field in form.fields:
            f = form[field].value()
            data.append(f.read())

        return HttpResponseRedirect(reverse_lazy(self.success_url))


class DecryptionKey(generic.TemplateView):
    template_name = "decryption_key.html"


class SelectAlgorithm(generic.FormView):
    form_class = SelectAlgorithmForm
    success_url = "base:index"
    template_name = "select_algorithm.html"

    def form_valid(self, form):
        return HttpResponseRedirect(reverse_lazy(self.success_url))
