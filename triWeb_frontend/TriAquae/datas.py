from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse


def TriAquaeData(request):
    # theme = "- Easy to Admin (v2.0.0)"
    return HttpResponse('{server:{load:80}}')


def getStatus():
    '''
    host, service, status, duration, attemp, last check, info
    status : 0-5, ok, warning, unknown, critical, pending
    '''
    dict_s = {'services': [{
            'Host': 'master',
            'Service': 'Memeory usage',
            'Status': 'Critical',
            'Duration': 6 * 60 * 1000 + 43 * 1000,
            'Attemp': 5,
            'Attemp_max': 5,
            'Last Check': 0,
            'Info': 'Socket timeout after 10 seconds'
        }, {
            'Host': 'master',
            'Service': 'test',
            'Status': 'Critical',
            'Duration': 3 * 3600 * 1000 + 6 * 60 * 1000 + 43 * 1000,
            'Attemp': 5,
            'Attemp_max': 5,
            'Last Check': 0,
            'Info': 'Socket timeout after 10 seconds'
        }, {
            'Host': '192.168.0.1',
            'Service': 'Port 26 Status',
            'Status': 'Critical',
            'Duration': 6 * 60 * 1000 + 43 * 1000,
            'Attemp': 5,
            'Attemp_max': 5,
            'Last Check': 0,
            'Info': 'Socket timeout after 10 seconds'
        }, {
            'Host': '192.168.0.2',
            'Service': 'test',
            'Status': 'Critical',
            'Duration': 3 * 3600 * 1000 + 6 * 60 * 1000 + 43 * 1000,
            'Attemp': 5,
            'Attemp_max': 5,
            'Last Check': 0,
            'Info': 'Socket timeout after 10 seconds'
        }
    ]}
    return dict_s
