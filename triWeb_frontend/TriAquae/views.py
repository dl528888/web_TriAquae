from django.template.loader import get_template
from django.template import Template, Context
from django.http import HttpResponse

import random
from collections import OrderedDict
try:
    import json
except:
    import simplejson as json


def TriAquae(request):
    t = get_template('index.html')
    # theme = "- Easy to Admin (v2.0.0)"

    html = t.render(Context({'theme': '- Easy to Admin (v2.0.0)'}))
    return HttpResponse(html)


def CpuUsage(request):
    dict_r = OrderedDict()
    random.seed()
    for i in range(24):
        now_i = '%d:05' % i
        val_i = random.randint(0, 100)
        dict_r[now_i] = val_i
    return HttpResponse(json.dumps(dict_r))


def ServiceStatus(request):
    from datas import getStatus
    dict_s = getStatus()
    dict_status = dict_s['services']
    if request.is_ajax():
        return HttpResponse(json.dumps(dict_status), mimetype="application/json")
    else:
        t = get_template('status.html')
        ss_summary = {
            'status': {
                'Ok': 0,
                'Critical': 0,
                'Warning': 0,
                'Unknown': 0,
                'Pending': 0
            },
            'handled': {
                'Unhandled': 0,
                'Problems': 0,
                'All': 0
            }
        }
        ss_detail = []
        for service in dict_status:
            ss_summary['handled']['All'] += 1
            status = service['Status']
            ss_summary['status'][status] += 1
            cell = []
            for k, v in service.iteritems():
                cell.append(v)
            ss_detail.append({'cell': cell})

        var_service_status = get_template('servicestatus.html').render(Context({
            'ss_summary_handled': ss_summary['handled'],
            'ss_summary_status': ss_summary['status'],
            'ss_detail': json.dumps(ss_detail)
        }))
        html = t.render(Context({
            'var_service_status': var_service_status
        }))
        return HttpResponse(html)
