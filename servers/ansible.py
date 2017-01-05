from models import Service, AnsibleLog
import subprocess
from threading import Thread
from django_cron import CronJobBase, Schedule


def execute(queryset):
    actionable_serv_ids = [obj.id for obj in queryset]
    actionable_services = Service.objects.filter(id__in=actionable_serv_ids)
    actionable_services = actionable_services.filter(execution='PENDING')

    # initial execution
    for service in actionable_services:
        service.thread = Thread(target=serviceExecute, args=(service,))
        service.thread.start()



def serviceExecute(service):
    cmd_template = 'ansible {server} -m win_service -a "name={name} state={state}"'

    # set execution
    service.execution = 'EXECUTING'
    initial_status = service.status

    # set status
    if service.action == 'START':
        service.status = 'STARTING'
        state = 'started'
    elif service.action == 'STOP':
        service.status = 'STOPPING'
        state = 'stopped'
    elif service.action == 'RESTART':
        service.status = 'RESTARTING'
        state = 'restarted'
    elif service.action == 'RELOAD':
        service.status = 'RELOADING'
        state = 'reloaded'

    service.save()


    cmd = cmd_template.format(server=service.server.getName(), name=service.name, state=state)

    # pokreni naredbu
    p = subprocess.Popen(cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)

    out, err = p.communicate()
    errcode = p.returncode

    # write to ansible log
    log_entry = AnsibleLog(
        service = service,
        cmd     = cmd,
        respone = out,
        error   = err,
        success = (False if err else True),
    )

    log_entry.save()


    # process response
    if out and 'SUCCESS' in out:
        service.execution = 'EXECUTED'
        # set status
        if service.action == 'START':
            service.status = 'STARTED'
        elif service.action == 'STOP':
            service.status = 'STOPED'
        elif service.action == 'RESTART':
            service.status = 'RESTARTED'
        elif service.action == 'RELOAD':
            service.status = 'RELOADED'
    else:
        service.status = initial_status
        service.execution = 'PENDING'

    service.save()




class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 1 minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'servers.my_cron_job'    # a unique code

    def do(self):
        actionable_services = Service.objects.all()
        actionable_services = actionable_services.filter(execution='PENDING')

        # initial execution
        for service in actionable_services:
            serviceExecute(service)
