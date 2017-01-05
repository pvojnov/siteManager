import sys
from django.contrib import messages, admin

from django.utils.html import format_html
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.template.response import TemplateResponse

import servers.ansible
from servers.models import AnsibleLog, Site, Server, ServiceType, ServiceContainer, Service



##################################################################
# ACTION ADMIN
##################################################################
class ActionAdmin(admin.ModelAdmin):
    # status display
    def status_alt(self, obj):
        if obj.status == 'STARTED':
            color = 'green'
        elif obj.status == 'STARTING':
            color = 'orange'
        elif obj.status == 'STOPPING':
            color = 'red'
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



    actions = ['start', 'stop', 'restart', 'reload', 'reset']

    # Dev - Temp
    def reset(self, request, queryset):
        for service in queryset:
            service.status = 'PENDING'
            service.action = 'NONE'
            service.execution = 'N_A'
            service.save()
    #reset.short_description = "reset values for "

    ##################################################################
    # Site Actions
    ##################################################################
    def start(self, request, queryset):
        form = None
        action = sys._getframe().f_code.co_name
        title = 'Start services'
        object_list_title = 'Following services will be started: '

        # remove objects that cannot be changed
        queryset = queryset.filter(active=True, action='NONE').exclude(execution__in=['PENDING', 'EXECUTING'])
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False, delete_change__status__in=[2, 3])
        #queryset = queryset.filter(active=True).exclude(servers__isnull=False)
        #queryset = queryset.filter(insert_change__status__in=[2])

        #return self.select_val_form(request, queryset, form, action, selection_item_title, object_list_title)

        if queryset.count() > 0:
            return self.confirm_action(request, queryset, form, action, title, object_list_title)
        else:
            messages.warning(request, 'There are no selected %s suitable for %s!' % (self.model._meta.verbose_name_plural.title(), action.title()))


    start.short_description = "Start services on selected sites"



    def stop(self, request, queryset):
        form = None
        action = sys._getframe().f_code.co_name
        title = '{action} services'.format(action=action.title())
        object_list_title = 'Following services will be stopped: '

        # remove objects that cannot be changed
        queryset = queryset.filter(active=True, action='NONE').exclude(execution__in=['PENDING', 'EXECUTING'])

        if queryset.count() > 0:
            return self.confirm_action(request, queryset, form, action, title, object_list_title)
        else:
            messages.warning(request, 'There are no selected %s suitable for %s!' % (self.model._meta.verbose_name_plural.title(), action.title()))

    stop.short_description = "Stop services on selected sites"

    def restart(self, request, queryset):
        form = None
        action = sys._getframe().f_code.co_name
        title = '{action} services'.format(action=action.title())
        object_list_title = 'Following services will be restarted: '

        # remove objects that cannot be changed
        queryset = queryset.filter(active=True, action='NONE').exclude(execution__in=['PENDING', 'EXECUTING'])

        if queryset.count() > 0:
            return self.confirm_action(request, queryset, form, action, title, object_list_title)
        else:
            messages.warning(request, 'There are no selected %s suitable for %s!' % (self.model._meta.verbose_name_plural.title(), action.title()))

    restart.short_description = "Restart services on selected sites"

    def reload(self, request, queryset):
        form = None
        action = sys._getframe().f_code.co_name
        title = '{action} services'.format(action=action.title())
        object_list_title = 'Following services will be reloaded: '

        # remove objects that cannot be changed
        queryset = queryset.filter(active=True, action='NONE').exclude(execution__in=['PENDING', 'EXECUTING'])

        if queryset.count() > 0:
            return self.confirm_action(request, queryset, form, action, title, object_list_title)
        else:
            messages.warning(request, 'There are no selected %s suitable for %s!' % (self.model._meta.verbose_name_plural.title(), action.title()))

    reload.short_description = "Reload services on selected sites"


    ##################################################################
    # confirmation form
    ##################################################################
    class AsignUserForm(forms.Form):
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

    def confirm_action(self, request, queryset, form, action, title, object_list_title):
        if 'confirm' in request.POST:
            form = self.AsignUserForm(request.POST)
            if form.is_valid():
                # do some action here
                for object in queryset:
                    # execute action on object
                    getattr(object, action)()
                    object.save()

                # execute ansible comands
                servers.ansible.execute(queryset)
                '''
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
                '''
            return HttpResponseRedirect(request.get_full_path())
        if not form:
            # adds action name to the form, necessary to return to the calling function after confirmation
            form = self.AsignUserForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})


        context = dict(
            self.admin_site.each_context(request),
            name=title,
            object_list_title=object_list_title,
            action=action,
            opts=self.model._meta,
            queryset=queryset,
            form=form,
        )

        return render(request, 'admin/form_action_confirmation.html', context)





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
    list_display = ['name', 'site', 'status_alt', 'action_alt', 'execution', 'environment', 'os', 'ip', 'hostname', 'ram', 'cpu', 'disk', 'description', 'active', ]
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
    list_display = ['name', 'server', 'status_alt', 'action_alt', 'execution', 'port', 'type', 'container', 'environment', 'created_on', 'started_on', 'reloaded_on', 'description', 'active', ]
    search_fields = ['name', 'server__site__name', 'server__name', 'port', 'type__name', 'container__name', 'environment', 'description', ]
    list_filter = ['server__site', 'server', 'type', 'status', 'action', 'container', 'environment', 'active', ]
admin.site.register(Service, ServiceAdmin)



##################################################################
# ANSIBLE
##################################################################

class AnslibleLogAdmin(ActionAdmin):
    save_on_top = True
    list_display = [ 'service', 'cmd', 'respone', 'error', 'success', 'created_on', ]
    search_fields = [ 'service__name', 'cmd', 'respone', 'error', 'success', 'created_on', ]
    list_filter = [ 'service__server__site', 'service__server', 'service', 'success', ]
admin.site.register(AnsibleLog, AnslibleLogAdmin)