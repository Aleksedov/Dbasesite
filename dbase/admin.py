from django.contrib import admin
from .models import *


class GuiltyInPersecutionsadmin(admin.TabularInline):
    model = GuiltyInPersecutions
    extra = 1

class ArtInPersadmin(admin.TabularInline):
    model = ArticlesInPersecution
    extra = 1

class ViolInPersadmin(admin.TabularInline):
    model = ViolationInPersecution
    extra = 1

class Persecutionadmin(admin.TabularInline):
    model = Perseqution
    extra = 1

class Guiltyadmin(admin.ModelAdmin):
    inlines = [GuiltyInPersecutionsadmin]

class Victimadmin(admin.ModelAdmin):
    inlines = [Persecutionadmin]

class Persequtionammine(admin.ModelAdmin):
    inlines = [GuiltyInPersecutionsadmin, ViolInPersadmin, ArtInPersadmin]

class Articleadmine(admin.ModelAdmin):
    radio_fields = {'code': admin.HORIZONTAL}



admin.site.register(Perseqution,Persequtionammine)
admin.site.register(Victim,Victimadmin)
admin.site.register(Guilty,Guiltyadmin)
admin.site.register(Place)
admin.site.register(Article,Articleadmine)
admin.site.register(Case)
admin.site.register(TypeOfPersecution)
admin.site.register(Violation)
admin.site.register(StatusOfVictimInPers)
admin.site.register(RestrictionOfVictim)
# Register your models here.
