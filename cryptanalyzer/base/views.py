# import json

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


def SelectAlgorithm(request, type):

    # if the previous form is in post, i.e. uploaded files present
    if request.method == "POST" and request.FILES:
        files_data = []
        files = request.FILES
        for f in files:
            file_data = {'name': files[f].name,
                         'content': str(files[f].read()),
                         'size': files[f].size / 1024.0
                         }
            files_data.append(file_data)

        request.session['files_data'] = files_data

        form = SelectAlgorithmForm()
        return render(request, "select_algorithm.html", {'form': form})

    elif request.method == "POST":
        key = request.POST['key']
        form = SelectAlgorithmForm(request.POST)
        algorithms = form['choice_field'].value()
        analyzer = utils.Analyzer(algorithms, key)
        files = analyzer.analyze(request.session['files_data'])

        request.session['files_data'] = files

    return HttpResponseRedirect(reverse_lazy("base:visual_analysis"))


class VisualAnalysis(generic.TemplateView):
    template_name = "graph.html"

    def get_context_data(self, *args, **kwargs):
        self.context = super(VisualAnalysis, self).get_context_data(*args, **kwargs)
        self.context['test'] = "swati"
        self.context['result'] = self.request.session['files_data']

        return self.context
