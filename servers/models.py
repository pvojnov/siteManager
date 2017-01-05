from django.db import models
from django.utils import timezone


##################################################################
# SITE
##################################################################
class Site(models.Model):
    name        = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active      = models.BooleanField(null=False, default=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(':'.join([str(self.id), (self.name or '(None)')]))



##################################################################
# SERVER
##################################################################
ENVIRONMENT = (
        ('DEV', 'Development'),
        ('TEST', 'Test'),
        ('PROD', 'Production'),
    )

STATUS = (
        ('STARTING', 'Starting'),
        ('STARTED', 'Started'),
        ('STOPPING', 'Stopping'),
        ('STOPPED', 'Stopped'),
        ('RESTARTING', 'Restarting'),
        ('RELOADING', 'Reloading'),
        ('PENDING', 'Pending'),
    )

ACTION = (
        ('START', 'Start'),
        ('STOP', 'Stop'),
        ('RESTART', 'Restart'),
        ('RELOAD', 'Reload'),
        ('NONE', 'None'),
    )

EXECUTION = (
        ('PENDING', 'Pending'),
        ('EXECUTING', 'Executing'),
        ('EXECUTED', 'Executed'),
        ('N_A', 'n/a'),
    )

class Server(models.Model):
    site        = models.ForeignKey(Site, null=False, blank=False, related_name='servers')
    environment = models.CharField(max_length=25, null=False, blank=False, choices=ENVIRONMENT)
    name        = models.CharField(max_length=100, null=True, blank=True)
    status      = models.CharField(max_length=25, null=False, blank=False, choices=STATUS, default='PENDING')
    action      = models.CharField(max_length=25, null=False, blank=False, choices=ACTION, default='NONE')
    execution   = models.CharField(max_length=25, null=False, blank=False, choices=EXECUTION, default='N_A')
    os          = models.CharField(max_length=25, null=False, blank=False, choices=(('LIN', 'Linux'), ('WIN', 'Windows')))
    ip          = models.GenericIPAddressField(null=False, blank=False)
    hostname    = models.CharField(max_length=100, null=True, blank=True)
    ram         = models.CharField(max_length=255, null=True, blank=True)
    cpu         = models.CharField(max_length=255, null=True, blank=True)
    disk        = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active      = models.BooleanField(null=False, default=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(':'.join([self.site.name, (self.name or str(self.id))]))



    def getName(self):
        return self.hostname or self.name






##################################################################
# SERVICE
##################################################################
class ServiceType(models.Model):
    name        = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active      = models.BooleanField(null=False, default=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(':'.join([str(self.id), (self.name or '(None)')]))


class ServiceContainer(models.Model):
    name        = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active      = models.BooleanField(null=False, default=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(':'.join([str(self.id), (self.name or '(None)')]))


class Service(models.Model):
    server      = models.ForeignKey(Server, null=False, blank=False)#, related_name='services')
    environment = models.CharField(max_length=25, null=False, blank=False, choices=ENVIRONMENT)
    name        = models.CharField(max_length=100, null=True, blank=True)
    status      = models.CharField(max_length=25, null=False, blank=False, choices=STATUS, default='PENDING')
    action      = models.CharField(max_length=25, null=False, blank=False, choices=ACTION, default='NONE')
    execution   = models.CharField(max_length=25, null=False, blank=False, choices=EXECUTION, default='N_A')
    description = models.TextField(null=True, blank=True)
    port        = models.IntegerField(null=False, blank=False, default=80)
    type        = models.ForeignKey(ServiceType, null=False, blank=False, related_name='services')
    container   = models.ForeignKey(ServiceContainer, null=False, blank=False, related_name='services')
    created_on  = models.DateTimeField(null=False, blank=False, default=timezone.now)
    started_on  = models.DateTimeField(null=True, blank=True)
    reloaded_on = models.DateTimeField(null=True, blank=True)
    active      = models.BooleanField(null=False, default=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(':'.join([self.server.site.name, (self.name or str(self.id))]))


    def start(self):
        self.action = 'START'
        self.execution = 'PENDING'
        print 'ansible {server} -m win_service -a "name={name} state=started"'.format(server=self.server.getName(), name=self.name)

    def stop(self):
        self.action = 'STOP'
        self.execution = 'PENDING'
        print 'ansible {server} -m win_service -a "name={name} state=stopped"'.format(server=self.server.getName(), name=self.name)

    def restart(self):
        self.action = 'RESTART'
        self.execution = 'PENDING'
        print 'ansible {server} -m win_service -a "name={name} state=restarted"'.format(server=self.server.getName(), name=self.name)

    def reload(self):
        self.action = 'RELOAD'
        self.execution = 'PENDING'
        print 'ansible {server} -m win_service -a "name={name} state=reloaded"'.format(server=self.server.getName(), name=self.name)






class AnsibleLog(models.Model):
    service     = models.ForeignKey(Service, null=True, blank=True)#, related_name='ansible_logs')
    cmd         = models.CharField(max_length=1000, null=False, blank=False)
    respone     = models.TextField(null=True, blank=True)
    error       = models.TextField(null=True, blank=True)
    success     = models.BooleanField(null=False, default=True)
    created_on  = models.DateTimeField(null=False, blank=False, default=timezone.now)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(':'.join([(unicode(self.service) or 'None'), (self.cmd or str(self.id))]))