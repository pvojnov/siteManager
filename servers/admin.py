from django.contrib import admin

from django.utils.html import format_html

from servers.models import Site, Server, ServiceType, ServiceContainer, Service



class SiteAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'description', 'active', ]
    search_fields = ['name', 'description', 'active', ]
    list_filter = ['active', ]

    def id_alt(self, obj):
        if obj.active:
            return obj.id
        else:
            return format_html('<span style="color: #{};">{}</span>',
                               'B25B5B',
                               obj.id)

    id_alt.allow_tags = True
    id_alt.short_description = 'ID'

    actions = ['start_site_services', 'stop_site_service', 'restart_site_service', 'reload_site_service']

    # Site Actions
    def start_site_services(self, request, queryset):
        form = None
        action = 'start_site_services'
        selection_item_title = 'Start site service: '
        object_list_title = 'Following services will be started: '

        print 'starting service'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    start_site_services.short_description = "Start services on selected sites"

    def stop_site_service(self, request, queryset):
        form = None
        action = 'stop_site_service'
        selection_item_title = 'Stop site service: '
        object_list_title = 'Following services will be stoped: '

        print 'starting service'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    stop_site_service.short_description = "Stop services on selected sites"

    def restart_site_service(self, request, queryset):
        form = None
        action = 'restart_site_service'
        selection_item_title = 'Restart site service: '
        object_list_title = 'Following services will be stoped: '

        print 'starting service'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    restart_site_service.short_description = "Restart services on selected sites"

    def reload_site_service(self, request, queryset):
        form = None
        action = 'reload_site_service'
        selection_item_title = 'Reload site service: '
        object_list_title = 'Following services will be reloaded: '

        print 'starting service'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    reload_site_service.short_description = "Reload services on selected sites"



admin.site.register(Site, SiteAdmin)



class ServerAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'site', 'envirnment', 'os', 'ip', 'hostname', 'ram', 'cpu', 'disk', 'description', 'active', ]
    search_fields = ['name', 'site__name', 'envirnment', 'os', 'ip', 'hostname', 'ram', 'cpu', 'disk', 'description', ]
    list_filter = ['site__name', 'envirnment', 'os', 'active', ]
admin.site.register(Server, ServerAdmin)


admin.site.register(ServiceType)
admin.site.register(ServiceContainer)


class ServiceAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['name', 'server', 'port', 'type', 'container', 'envirnment', 'created_on', 'started_on', 'reloaded_on', 'description', 'active', ]
    search_fields = ['name', 'server__site__name', 'server__name', 'port', 'type__name', 'container__name', 'envirnment', 'description', ]
    list_filter = ['server__site', 'server', 'type', 'container', 'envirnment', 'active', ]
admin.site.register(Service, ServiceAdmin)
