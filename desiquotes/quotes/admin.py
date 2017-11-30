from django.contrib import admin
from desiquotes.quotes.models import Quote
from django.contrib.contenttypes.admin import GenericTabularInline


admin.site.register(Quote)

# Register your models here.
