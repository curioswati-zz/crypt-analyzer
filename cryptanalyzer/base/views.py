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


def SelectAlgorithm(request, analysis_type, varying):
    if request.method == "GET":
        request.session['analysis_type'] = analysis_type
        request.session['varying'] = varying

        form = SelectAlgorithmForm()

        return render(request, "select_algorithm.html", {'form': form})

    elif request.method == "POST":
        form = SelectAlgorithmForm(request.POST)
        request.session['algorithms'] = form['choice_field'].value()

        if request.session['varying'] == 'file_size':
            return HttpResponseRedirect(reverse_lazy("base:vary_file_size"))

        elif request.session['varying'] == 'key_size':
            return HttpResponseRedirect(reverse_lazy("base:vary_key_size"))


def VaryFileSize(request):
    if request.method == "GET":
        form = UploadFileForm()
        analysis_type = request.session['analysis_type']
        algorithms = request.session['algorithms']

        if 'des' in algorithms:
            keylen = 24
        elif 'aes' in algorithms:
            keylen = 32
        else:
            keylen = 56

        return render(request, "varying_file_size.html",
                      {'form': form,
                       'analysis_type': analysis_type,
                       'keylen': keylen
                       })

    else:
        key = request.POST['key']
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            files_data = []
            files = form.cleaned_data
            for entry in files:
                file_data = {'name': files[entry].name,
                             'content': str(files[entry].read()),
                             'size': files[entry].size / 1024.0
                             }
                files_data.append(file_data)

            algorithms = request.session['algorithms']
            analyzer = utils.Analyzer()
            files = analyzer.analyze_varying_data(request.session['analysis_type'],
                                                  algorithms, key, files_data)

            # to pass requied variables to next view
            request.session['files_data'] = files

        return HttpResponseRedirect(reverse_lazy("base:visual_analysis"))


def VaryKeySize(request):
    if request.method == "GET":
        form = UploadFileForm()
        analysis_type = request.session['analysis_type']
        algorithms = request.session['algorithms']

        if 'des' in algorithms:
            keylen = 24
        elif 'aes' in algorithms:
            keylen = 32
        else:
            keylen = 56

        return render(request, "varying_key_size.html",
                      {'form': form,
                       'analysis_type': analysis_type,
                       'keylen': keylen
                       })

    else:
        data = request.FILES['data'].read()
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            key_files_data = []
            files = form.cleaned_data
            for entry in files:
                file_data = {'name': files[entry].name,
                             'content': str(files[entry].read()),
                             'size': files[entry].size / 1024.0
                             }
                key_files_data.append(file_data)

            algorithms = request.session['algorithms']
            analyzer = utils.Analyzer()
            files = analyzer.analyze_varying_key(request.session['analysis_type'],
                                                 algorithms, data, key_files_data)

            # to pass requied variables to next view
            request.session['files_data'] = files

        return HttpResponseRedirect(reverse_lazy("base:visual_analysis"))


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
