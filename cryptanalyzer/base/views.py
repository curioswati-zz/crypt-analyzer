# import json

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


class DecryptionKey(generic.TemplateView):
    template_name = "decryption_key.html"


def SelectAlgorithm(request, analysis_type):

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
        analyzer = utils.Analyzer()
        files = analyzer.analyze(analysis_type, algorithms, key, request.session['files_data'])

        # to pass requied variables to next view
        request.session['algorithms'] = algorithms
        request.session['files_data'] = files

        return HttpResponseRedirect(reverse_lazy("base:visual_analysis"))

    else:
        form = SelectAlgorithmForm()
        return render(request, "select_algorithm.html", {'form': form})


def VisualAnalysis(request):
    """
    result page
    """
    result = request.session['files_data']
    result = sorted(result, key=lambda x: x['size'])

    algorithms = request.session['algorithms']

    xdata = [x['size'] for x in result]
    chartdata = {'x': xdata, 'name1': 'Encryption Time in sec'}

    for i, algo in enumerate(algorithms):
        chartdata['y%d' % int(i+1)] = [x[algo+'_time'] for x in result]
        chartdata['name%d' % int(i+1)] = algo.capitalize() + " Encryption Time"

    charttype = "lineChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': 'linechart_container',
        'extra': {
            'x_is_date': False,
            'x_axis_format': ".03f",
            'y_axis_format': ".06f",
            'tag_script_js': True
        },
        'result': result
    }

    return render_to_response('result.html', data)
