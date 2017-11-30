from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from desiquotes.quotes.models import Quote
from django.utils.translation import ugettext_lazy as _
from autoslug import AutoSlugField

class Author(models.Model):
    name = models.CharField(_('author name'), max_length=50, blank=False)
    slug = AutoSlugField(populate_from='name')
    avatar = models.ImageField(upload_to='author/avatars/', null=True, blank=True)
    likes = models.IntegerField(default=0)
    writer  = GenericRelation(Quote)

    def __str__(self): # __str__ for Python 3, __unicode__ for Python 2
        return self.name
