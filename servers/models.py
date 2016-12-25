from django.db import models
from django.utils import timezone



class Site(models.Model):
    name        = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    active      = models.BooleanField(null=False, default=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(':'.join([str(self.id), (self.name or '(None)')]))


ENVIRONMENT = (
        ('DEV', 'Development'),
        ('TEST', 'Test'),
        ('PROD', 'Production'),
    )

class Server(models.Model):
    site        = models.ForeignKey(Site, null=False, blank=False, related_name='servers')
    envirnment  = models.CharField(max_length=25, null=False, blank=False, choices=ENVIRONMENT)
    name        = models.CharField(max_length=100, null=True, blank=True)
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
    envirnment  = models.CharField(max_length=25, null=False, blank=False, choices=ENVIRONMENT)
    name        = models.CharField(max_length=100, null=True, blank=True)
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