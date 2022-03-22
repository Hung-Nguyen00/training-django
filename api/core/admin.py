from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.redirects.models import Redirect
# Register your models here.


admin.site.unregister(Site)
admin.site.unregister(Redirect)