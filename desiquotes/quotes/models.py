from django.db import models

#from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
#from autoslug import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count

#import markdown
from taggit.managers import TaggableManager

@python_2_unicode_compatible
class Quote(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )

    content = models.TextField(max_length=4000)
    tags = TaggableManager()
    likes = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quotes")
        ordering = ("-create_date",)

    def __str__(self):
        return self.content
    """
    def get_content_as_markdown(self):
        return markdown.markdown(self.content, safe_mode='escape')
    """	
    @staticmethod
    def get_published():
        quotes = Quote.objects.filter(status=Quote.PUBLISHED)
        return quotes

    @staticmethod
    def get_counted_tags():
        tag_dict = {}
        query = Quote.objects.filter(status='P').annotate(tagged=Count(
            'tags')).filter(tags__gt=0)
        for obj in query:
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:  # pragma: no cover
                    tag_dict[tag] += 1

        return tag_dict.items()

    def get_summary(self):
        if len(self.content) > 255:
            return '{0}...'.format(self.content[:255])
        else:
            return self.content
    
    @property
    def get_tags(self):
        return self.tags.slugs()
  
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Quote._meta.fields]

"""
    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')
"""
