from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse_lazy

#import markdown
from desiquotes.quotes.forms import QuoteForm
from desiquotes.quotes.models import Quote
from desiquotes.decorators import ajax_required


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

    return render(request, 'quotes/quotes.html', {
        'quotes': quotes,
        'popular_tags': popular_tags
    })


class CreateQuote(LoginRequiredMixin, CreateView):
    """
    """
    template_name = 'quotes/write.html'
    form_class = QuoteForm
    success_url = reverse_lazy('quotes')

    def form_valid(self, form):
        form.instance.create_user = self.request.user
        return super(CreateQuote, self).form_valid(form)


class EditQuote(LoginRequiredMixin, UpdateView):
    template_name = 'quotes/edit.html'
    model = Quote
    form_class = QuoteForm
    success_url = reverse_lazy('quotes')


@login_required
def quotes(request):
    all_quotes = Quote.get_published()
    return _quotes(request, all_quotes)


@login_required
def quote(request, slug):
    quote = get_object_or_404(Quote, slug=slug, status=Quote.PUBLISHED)
    return render(request, 'quotes/quote.html', {'quote': quote})


@login_required
def tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name).filter(status='P')
    return _quotes(request, quotes)


@login_required
def drafts(request):
    drafts = Quote.objects.filter(create_user=request.user,
                                    status=Quote.DRAFT)
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


"""
@login_required
@ajax_required
def comment(request):
    try:
        if request.method == 'POST':
            quote_id = request.POST.get('quote')
            quote = Quote.objects.get(pk=quote_id)
            comment = request.POST.get('comment')
            comment = comment.strip()
            if len(comment) > 0:
                quote_comment = QuoteComment(user=request.user,
                                                 quote=quote,
                                                 comment=comment)
                quote_comment.save()
            html = ''
            for comment in quote.get_comments():
                html = '{0}{1}'.format(html, render_to_string(
                    'quotes/partial_quote_comment.html',
                    {'comment': comment}))

            return HttpResponse(html)

        else:
            return HttpResponseBadRequest()

    except Exception:
        return HttpResponseBadRequest()
"""
