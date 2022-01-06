from django import template
from django.db.models import Q
from blog.models import Notification, News, Post, Category, Question, About
from blog.forms import PostSearchForm
from itertools import chain
from django.urls import reverse


register = template.Library()

@register.inclusion_tag('blog/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    author = request_user.author
    notifications = Notification.objects.filter(to_author=author).exclude(author_has_seen=True).exclude(title__isnull=False).order_by('-date')
    news_notification = Notification.objects.filter(to_author = author).exclude(author_has_seen=True).exclude(title = None).order_by('-date')
    not_count = notifications.count() + news_notification.count()
    return {'notifications': notifications, 'n_not':news_notification, 'nc':not_count}

@register.inclusion_tag('blog/search.html', takes_context=True)
def post_search(context):
    request_user = context['request'].user
    request = context['request']
    form = PostSearchForm()
    categories = Category.objects.all()
    results = []

            

    return {'form': form, 'results': results, 'categories':categories}
    
@register.inclusion_tag('blog/social.html', takes_context=True)
def show_social(context):
    about = About.objects.all()[:1]
    return {'about': about}
    
'''
@register.simple_tag
def anchor(url_name, section_id, notification_pk, pk, slug_text):
    notification = Notification.objects.get(id=notification_pk)
    article = Post.objects.get(id=pk, slug=slug_text)

    return reverse(url_name) + '#' + section_id
'''