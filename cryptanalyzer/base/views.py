from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from .forms import UploadFileForm, SelectAlgorithmForm
from . import utils


class IndexView(generic.TemplateView):
    template_name = "index.html"


class ContactView(generic.TemplateView):
    template_name = "index.html"


class EncryptionData(generic.FormView):
    form_class = UploadFileForm
    success_url = "base:select_algorithm"
    template_name = "encryption_data.html"


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


files = []


def SelectAlgorithm(request, type):
    global files
    if request.method == "POST" and request.FILES:
        files = request.FILES
        form = SelectAlgorithmForm()
        return render(request, "select_algorithm.html", {'form': form})

    elif request.method == "POST":
        form = SelectAlgorithmForm(request.POST)
        utils.encrypt(files, form['choice_field'].value())

    return HttpResponseRedirect(reverse_lazy("base:index"))
