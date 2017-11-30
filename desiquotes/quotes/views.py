from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy

from desiquotes.activities.models import Activity
from django.contrib.contenttypes.models import ContentType


#import markdown
from desiquotes.quotes.forms import QuoteForm
from desiquotes.quotes.models import Quote
from desiquotes.decorators import ajax_required
import pprint
import numpy as np


def _quotes(request, quotes):
    paginator = Paginator(quotes, 10)
    page = request.GET.get('page')
    try:
        quotes = paginator.page(page)

    except PageNotAnInteger:
        quotes = paginator.page(1)

    except EmptyPage:   # pragma: no cover
        quotes = paginator.page(paginator.num_pages)

    popular_tags = Quote.get_counted_tags()

    return {
        'quotes': quotes,
        'popular_tags': popular_tags
    }

class CreateUserQuote(LoginRequiredMixin, CreateView):
    template_name = 'quotes/add_user_quote.html'
    form_class = QuoteForm
    success_url = reverse_lazy('quotes:quotes')

    def form_valid(self, form):
        #form.instance.create_user = self.request.user
        form.instance.content_object = self.request.user
        form.instance.object_id = self.request.user.id 
        form.instance.writer_type = Quote.USER

        return super(CreateUserQuote, self).form_valid(form)


class EditUserQuote(LoginRequiredMixin, UpdateView):
    template_name = 'quotes/edit_user_quote.html'
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy('quotes:quotes')

class CreateAuthorQuote(LoginRequiredMixin, CreateView):
    success_url = reverse_lazy('quotes:quotes')

class EditAuthorQuote(LoginRequiredMixin, UpdateView):
    success_url = reverse_lazy('quotes:quotes')

def home(request):
    quotes = Quote.get_published()
    return  render(request, 'quotes/quotes.html', _quotes(request, quotes))

@login_required
def user_quotes(request, name=None):
    logged_in_user = request.user
    quotes = Quote.get_user_published(logged_in_user)
    return  render(request, 'quotes/quotes.html', _quotes(request, quotes))

@login_required
def quote(request, slug):
    quote = get_object_or_404(Quote, slug=slug, status=Quote.PUBLISHED)
    return render(request, 'quotes/quote.html', {'quote': quote})


@login_required
def tag(request, tag_name):
    #quotes = Quote.objects.filter(tags__name=tag_name).filter(status='P')
    quotes = Quote.get_published(tag_name=tag_name)
    return render(request, 'quotes/quotes.html', _quotes(request, quotes))


@login_required
def drafts(request):
    #drafts = Quote.objects.filter(create_user=request.user, status=Quote.DRAFT)
    drafts = Quote.objects.filter(object_id=request.user.id, status=Quote.DRAFT)
    return render(request, 'quotes/drafts.html', {'drafts': drafts})


@login_required
@ajax_required
def preview(request):
    try:
        if request.method == 'POST':
            content = request.POST.get('content')
            html = 'Nothing to display :('
            if len(content.strip()) > 0:
                #html = markdown.markdown(content, safe_mode='escape')
                html = content

            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()


@login_required
@ajax_required
def remove(request):
    try:
        quote_id = request.POST.get('quote')
        quote = Quote.objects.get(pk=quote_id)
        #if quote.create_user == request.user:
        if quote.object_id == request.user.id:
            """ 
            likes = quote.get_likes()
            for like in likes:
                like.delete()
            """
            quote.delete()
            return HttpResponse()
        else:
            return HttpResponseForbidden()
    except Exception:
        return HttpResponseBadRequest()

@login_required
@ajax_required

def like(request):
    quote_id = request.POST['quote']
    quote    = Quote.objects.get(pk=quote_id)
    user     = request.user
    #like    = QuoteActivity.objects.filter(activity_type=QuoteActivity.LIKE, quote=quote_id, user=user)
    #like    = quote.likes.filter(activity_type=Activity.LIKE, user=user)
    try:
        like = Activity.objects.get(content_type=ContentType.objects.get_for_model(quote), object_id=quote.id, user=request.user)

        if like:
            """
            user.profile.unotify_liked(quote)
	    """
            like.delete()
            #Activity.objects.delete(content_object=quote, activity_type=Activity.LIKE, user=request.user)
        else:
            #like = QuoteActivity(activity_type=QuoteActivity.LIKE, quote=quote, user=user)
            #like.save()
            #quote.likes.create(activity_type=Activity.LIKE, user=user)
            like = Activity(activity_type=Activity.LIKE, content_object=quote, user=request.user)
            like.save()
            """
            user.profile.notify_liked(quote)
    	    """
    except Activity.DoesNotExist:
        quote.likes.create(activity_type=Activity.LIKE, user=user)
	
    #return HttpResponse(quote.calculate_likes())
    return HttpResponse(quote.likes.count())
