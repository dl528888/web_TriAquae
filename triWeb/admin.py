from django.contrib import admin
#from books.models import Publisher,Author,Book
from triWeb.models import IP,User,Group,MonitorMethod,MonthlyWeatherByCity,PingStatusValue,DailyWeather,ConnectionMethod,HostLog
class AuthorAdmin(admin.ModelAdmin):
	list_display = ('first_name','last_name','email')
	search_fields =  ('first_name','last_name')
class BookAdmin(admin.ModelAdmin):
	list_display = ('title','publisher','publication_date')
	list_filter = ('publication_date',)
	date_hierarchy = 'publication_date'
	ordering = ('-publication_date',)
	fields = ('title','publisher','authors','publication_date')
	filter_vertical = ('authors',)
	raw_id_fields = ('publisher',)

class IpAdmin(admin.ModelAdmin):
	list_display = ('ip','server_name','opreating_system','status')
	search_fields = ('ip','server_name','opreating_system')
class GroupAdmin(admin.ModelAdmin):
	list_display = ('group_name','parent_group')

class PingStatusAdmin(admin.ModelAdmin):
	list_display = ('ip','ping_value')

class HostLogAdmin(admin.ModelAdmin):
	list_display = ('ip','event_type','cmd','event_log','result','note','track_mark')
	list_filter = ('track_mark','ip','event_type','result')


admin.site.register(IP,IpAdmin)
admin.site.register(User)
admin.site.register(Group,GroupAdmin)
admin.site.register(MonitorMethod)
admin.site.register(MonthlyWeatherByCity)
admin.site.register(PingStatusValue,PingStatusAdmin)
admin.site.register(DailyWeather)
admin.site.register(ConnectionMethod)
admin.site.register(HostLog,HostLogAdmin)
