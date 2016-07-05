# import json
import random
import time
import datetime

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
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


def VisualAnalysis(request):
    """
    lineChart page
    """
    start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    nb_element = 100
    xdata = range(nb_element)
    xdata = list(map(lambda x: start_time + x * 1000000000, xdata))
    ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    ydata2 = list(map(lambda x: x * 2, ydata))

    tooltip_date = "%d %b %Y %H:%M:%S %p"
    extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"},
                   "date_format": tooltip_date}
    chartdata = {'x': xdata,
                 'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
                 'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie}
    charttype = "lineChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': 'linechart_container',
        'extra': {
            'x_is_date': True,
            'x_axis_format': "%d %b %Y %H",
            'tag_script_js': True,
        },
        'result': request.session['files_data']
    }

    return render_to_response('result.html', data)
