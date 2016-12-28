from django.contrib import messages, admin

from django.utils.html import format_html
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from servers.models import Site, Server, ServiceType, ServiceContainer, Service



##################################################################
# ACTION ADMIN
##################################################################
class ActionAdmin(admin.ModelAdmin):
    # status display
    def status_alt(self, obj):
        if obj.status == 'STARTED':
            color = 'green'
        elif obj.status == 'STOPPED':
            color = 'red'
        elif obj.status == 'RESTARTING':
            color = 'orange'
        elif obj.status == 'RELOADING':
            color = 'purple'
        elif obj.status == 'PENDING':
            color = 'blue'

        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )

    status_alt.allow_tags = True
    status_alt.short_description = 'STATUS'

    # action display
    def action_alt(self, obj):
        if obj.action == 'START':
            color = 'green'
        elif obj.action == 'STOP':
            color = 'red'
        elif obj.action == 'RESTART':
            color = 'orange'
        elif obj.action == 'RELOAD':
            color = 'purple'
        elif obj.action == 'NONE':
            color = 'blue'

        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_action_display()
        )

    action_alt.allow_tags = True
    action_alt.short_description = 'ACTION'



    actions = ['start_services', 'stop_services', 'restart_services', 'reload_services']

    # Site Actions
    def start_services(self, request, queryset):
        form = None
        action = 'start_services'
        selection_item_title = 'Start site service: '
        object_list_title = 'Following services will be started: '

        print 'starting services'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False)
        #queryset = queryset.filter(insert_change__status__in=[2])

        return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    start_services.short_description = "Start services on selected sites"

    def stop_services(self, request, queryset):
        form = None
        action = 'stop_services'
        selection_item_title = 'Stop services: '
        object_list_title = 'Following services will be stoped: '

        print 'starting services'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    stop_services.short_description = "Stop services on selected sites"

    def restart_services(self, request, queryset):
        form = None
        action = 'restart_services'
        selection_item_title = 'Restart services: '
        object_list_title = 'Following services will be stoped: '

        print 'starting service'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    restart_services.short_description = "Restart services on selected sites"

    def reload_services(self, request, queryset):
        form = None
        action = 'reload_site_services'
        selection_item_title = 'Reload site service: '
        object_list_title = 'Following services will be reloaded: '

        print 'starting services'

        # remove objects that cannot be changed
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

    reload_services.short_description = "Reload services on selected sites"



    def select_val_form(self, request, queryset, form, action, selection_item_title, object_list_title):
        if 'apply' in request.POST:
            form = self.AsignUserForm(request.POST)
            if form.is_valid():
                change = form.cleaned_data['change']
                if action == 'copy_for_update':
                    for i in queryset:
                        i.pk = None
                        i.insert_change = change
                        i.active = False
                        i.save()
                    messages.success(request, 'Objects created for update using change %s. Objects: %s' % (change.id, queryset.values_list('sufi',flat=True)[:20]))
                elif action == 'set_delete_change':
                    queryset.update(delete_change=change)
                    messages.success(request, 'Change %s applied as delete change to objects %s.' % (change.id, queryset.values_list('sufi',flat=True)[:20]))
            return HttpResponseRedirect(request.get_full_path())
        if not form:
            form = self.AsignUserForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})
        return render_to_response('admin/select_change.html', {'objects': queryset,
                                                         'asign_user_form': form,
                                                         'action': action,
                                                         'selection_item_title': selection_item_title,
                                                         'object_list_title': object_list_title,
                                                        },
                                  context_instance=RequestContext(request))

    class AsignUserForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        change = forms.ModelChoiceField(Change.objects.exclude(status__id__in=[2,3]))




##################################################################
# SITE
##################################################################
class SiteAdmin(ActionAdmin):
    save_on_top = True
    list_display = ['name', 'description', 'active', ]
    search_fields = ['name', 'description', 'active', ]
    list_filter = ['active', ]

admin.site.register(Site, SiteAdmin)


##################################################################
# SERVER
##################################################################
class ServerAdmin(ActionAdmin):
    save_on_top = True
    list_display = ['name', 'site', 'status_alt', 'action_alt', 'environment', 'os', 'ip', 'hostname', 'ram', 'cpu', 'disk', 'description', 'active', ]
    search_fields = ['name', 'site__name', 'environment', 'os', 'ip', 'hostname', 'ram', 'cpu', 'disk', 'description', ]
    list_filter = ['site__name', 'environment', 'status', 'action', 'os', 'active', ]
admin.site.register(Server, ServerAdmin)


admin.site.register(ServiceType)
admin.site.register(ServiceContainer)

##################################################################
# SERVICE
##################################################################
class ServiceAdmin(ActionAdmin):
    save_on_top = True
    list_display = ['name', 'server', 'status_alt', 'action_alt', 'port', 'type', 'container', 'environment', 'created_on', 'started_on', 'reloaded_on', 'description', 'active', ]
    search_fields = ['name', 'server__site__name', 'server__name', 'port', 'type__name', 'container__name', 'environment', 'description', ]
    list_filter = ['server__site', 'server', 'type', 'status', 'action', 'container', 'environment', 'active', ]
admin.site.register(Service, ServiceAdmin)
