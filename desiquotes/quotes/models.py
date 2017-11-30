from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
#from autoslug import AutoSlugField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
from desiquotes.activities.models import Activity
from django.contrib.contenttypes.fields import GenericRelation


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
 
    USER = 'U'
    AUTHOR = 'A'
    WRITER_CHOICES = ( 
        (USER, 'User'),
        (AUTHOR, 'Author'),
    )

    content = models.TextField(max_length=4000)
    tags = TaggableManager()
    #likes = models.IntegerField(default=0)
    likes = GenericRelation(Activity)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    writer_type = models.CharField(max_length=1, choices=WRITER_CHOICES, default=USER)
    #create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    update_user = models.ForeignKey(User, null=True, blank=True, related_name="+")

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id    = models.PositiveIntegerField(null=True)
    content_object     = GenericForeignKey('content_type', 'object_id')

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
    def get_published(tag_name=None):
        if tag_name is None:
            quotes = Quote.objects.filter(status=Quote.PUBLISHED)
        else:
            quotes = Quote.objects.filter(tags__name=tag_name).filter(status='P')
        return quotes    

    def get_user_published(self,tag_name=None):
        if tag_name is None:
            #quotes = Quote.objects.filter(status=Quote.PUBLISHED,create_user=self.pk)
            quotes = Quote.objects.filter(status=Quote.PUBLISHED,object_id=self.pk)
        else:
            #quotes = Quote.objects.filter(tags__name=tag_name).filter(status=Quote.PUBLISHED,create_user=self.pk)
            quotes = Quote.objects.filter(tags__name=tag_name).filter(status=Quote.PUBLISHED,object_id=self.pk)
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

    def calculate_likes(self):
        #likes = QuoteActivity.objects.filter(activity_type=QuoteActivity.LIKE, quote=self.pk).count()
        #self.likes = likes
        #self.save()
        return self.likes.count()
  
    def get_likes(self):
        #likes = QuoteActivity.objects.filter(activity_type=QuoteActivity.LIKE, quote=self.pk)
        #quote=self.pk
        #likes = quote.likes.filter(activity_type=Activity.LIKE)
        return self.likes.count()
        #return likes 

    def get_likers(self):
        likes = self.get_likes()
        likers = []
        for like in likes:
            likers.append(like.user)
        return likers	

    @property
    def get_tags(self):
        return self.tags.slugs()

    def get_writer_type(self):
        return self.writer_type

    """
    def get_tags(self):
        return Tag.objects.filter(quote=self)
    """

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Quote._meta.fields]

    """
    def get_summary_as_markdown(self):
        return markdown.markdown(self.get_summary(), safe_mode='escape')
    """
@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    quote = models.ForeignKey(Quote)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'quote'),)
        index_together = [['tag', 'quote'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            if tag.quote.status == Quote.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]
