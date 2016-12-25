import os

from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.views import generic

from .forms import UploadFileForm, SelectAlgorithmForm
from .utils import analyzer, utils


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
    # to show decrypt button initially
    request.session['show_decrypt'] = True

    if request.method == "GET":
        form = UploadFileForm()
        algorithms = request.session['algorithms']

        # fix minimum keylength to allow
        if 'rc6' in algorithms:
            keylen = 16
        elif 'des' in algorithms:
            keylen = 24
        elif 'twofish' in algorithms or 'aes' in algorithms:
            keylen = 32
        else:
            keylen = 56

        return render(request, "varying_file_size.html", {'form': form,
                                                          'keylen': keylen
                                                          })

    else:
        key = request.POST['key']
        request.session['key'] = key
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
            analyzer_obj = analyzer.Analyzer()
            files = analyzer_obj.encrypt_varying_data(algorithms, key, files_data)

            # to pass requied variables to next view
            request.session['files_data'] = files

        return HttpResponseRedirect(reverse_lazy("base:visual_analysis"))


def VaryKeySize(request):
    # to show decrypt button initially
    request.session['show_decrypt'] = True

    if request.method == "GET":
        form = UploadFileForm()
        algorithms = request.session['algorithms']

        # fix minimum keylength to allow
        if 'des' in algorithms:
            keylen = 24
        elif 'twofish' in algorithms or 'aes' in algorithms:
            keylen = 32
        else:
            keylen = 56

        return render(request, "varying_key_size.html", {'form': form,
                                                         'keylen': keylen
                                                         })

    else:
        data_file = request.FILES['data']
        data_file_name = data_file.name
        data = data_file.read()
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
            analyzer_obj = analyzer.Analyzer()
            files = analyzer_obj.encrypt_varying_key(algorithms, data,
                                                     key_files_data, data_file_name)

            # to pass requied variables to next view
            request.session['files_data'] = files

        return HttpResponseRedirect(reverse_lazy("base:visual_analysis"))


def VisualAnalysis(request):
    """
    result page
    """
    result = request.session['files_data']
    result = sorted(result, key=lambda x: x['size'])

    sysconfig = utils.get_system_config()
    analysis_type = request.session['analysis_type'].capitalize()

    algorithms = request.session['algorithms']

    xdata = [x['size'] for x in result]
    chartdata = {'x': xdata, 'name1': analysis_type + ' Time in sec'}

    for i, algo in enumerate(algorithms):
        chartdata['y%d' % int(i+1)] = [x[algo+'_time'] for x in result]
        name = algo.capitalize() + " " + analysis_type + " Time"
        chartdata['name%d' % int(i+1)] = name

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
        'result': result,
        'sysconfig': sysconfig,
        'show_decrypt': request.session['show_decrypt']
    }

    return render_to_response('result.html', data)


def Decrypt(request):
    '''
    decrypted encrypted files.
    '''
    request.session['show_decrypt'] = False

    files_data = request.session['files_data']
    algorithms = request.session['algorithms']
    key = request.session['key']

    request.session['analysis_type'] = "decryption"

    analyzer_obj = analyzer.Analyzer()

    if request.session['varying'] == 'file_size':
        result = analyzer_obj.decrypt_varying_data(algorithms, key, files_data)
    elif request.session['varying'] == 'key_size':
        result = analyzer_obj.decrypt_varying_key(algorithms, files_data)

    request.session['files_data'] = result

    return HttpResponseRedirect(reverse_lazy("base:visual_analysis"))
