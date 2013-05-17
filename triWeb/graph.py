from django.shortcuts import render_to_response
from django.http import HttpResponse
from triWeb.models import IP,MonthlyWeatherByCity,DailyWeather,PingStatusValue
from chartit import DataPool,Chart
from chartit import PivotDataPool,PivotChart
import json

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def weather_chart_view(request):
	weatherdata = \
		DataPool(
		  series=
			[{'options':{
				'source':MonthlyWeatherByCity.objects.all()},
				
			  'terms':[
				'month',
				'Bejing_temp',
				'ShangHai_temp']}
				

			]
		)
	cht = Chart(
		datasource = weatherdata,
		series_options = 
		[{'options':{
			'type':'area',
			'stacking':False,
			    },
		
		  'terms':{
			'month':[
				'Bejing_temp','ShangHai_temp'
				]
			}
		}],
		chart_options = 
			{'title':{
				'text': 'weather data of Bejing and ShangHai',},
			'xAxis':{
				'title':{'test':"Month number"}
				}
			}
		)
	return render_to_response('highchart.html',{'weatherchart':cht})

def ping_status_view(request):
	ds = DataPool(
		series = 
			[{'options':{

				'source': PingStatusValue.objects.filter(ip=IP.objects.get(ip='8.8.8.8'))},
			 'terms': [
				('check_time', lambda d: check_time.mktime(d.timetuple())),'ping_value']
			}]
			
		)
	cht = Chart(
		datasource = ds,
		series_options = 
			[{'options':{
				'type': 'line',
				'stacking': False},
			 'terms':{
				'check_time':[
					'ping_value']}	

			}],
		chart_options = 
			{'title':{
				'text':'ping_value status'},
			'xAxis': {

				'title':{
					'text':'check date'}}}
		)
	return render_to_response('highchart2.html',{'pingChart':cht})
