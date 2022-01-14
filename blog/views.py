from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
from django.core.files.storage import FileSystemStorage
from django.views.generic import View, TemplateView, ListView, DetailView, RedirectView
from django.core.paginator import Paginator
from django.db.models import Q
from django.core import serializers
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from . decorators import unauthenticated_user, allowed_users, admin_only
from . models import *
from . forms import PostForm, RegisterForm, NewsForm, QuestionForm, CommentForm, ReplyForm, ProfileForm, PostSearchForm, ContactForm 

from . utils import generate_token
from itertools import chain
import sweetify
import os
import threading

# Create your views here.

#------------------------------------------------------------------------
# REGISTRATION AND LOGIN
#---------------------------------------------------------------------------

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('blog/activate.html', {
        'user':user, 
        'domain':current_site, 
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject = email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER,
    to = [user.email]
    
    )

    EmailThread(email).start()

@unauthenticated_user
def registerPage(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            send_activation_email(user, request)

            message = sweetify.success(request, title='Account Created', text='We\'ve sent you an email to verify your account', icon='success', button='Ok', timer=4000)

            return redirect('login')

    context = {'form':form}
    
    return render(request, 'blog/reg.html', context)        

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_verified:
                login(request, user)
                sweetify.success(request, title='Success', text='You\'re now logged in', icon='success', button='Ok', timer=3000)
                return redirect(request.GET.get('next', '/'))
            else:
                sweetify.warning(request, title='Warning', text='Email is not verified. Please check your email inbox or spam for verification link', icon='warning', button='Ok', timer=4000)
                return redirect('login')
        else:
            sweetify.error(request, title='Error', text='Your email OR password is incorrect', icon='error', button='Ok', timer=3000)
    context = {}
    return render(request, 'blog/log.html', context)

@login_required
def logoutUser(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))

def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_verified = True
        user.save()

        sweetify.success(request, title='Success', text='Email verified, You can now log in', icon='success', button='Ok', timer=3000)

        return redirect(reverse('login'))

    return render(request, 'blog/activate_failed.html', {"user": user})

#---------------------------------------------------------------------------------
# COMMENTS & REPLIES MANAGEMENT
#--------------------------------------------------------------------------------
@admin_only
def comments_management(request):
    comm_total = Comment.objects.all()
    rep_total = Reply.objects.all()
    comments = Comment.objects.all().order_by('-date_commented')[:15]
    replies = Reply.objects.all().order_by('-date_replied')[:15]

    context = {'comments':comments, 'com':comm_total, 'rep':rep_total, 'replies':replies}
    return render(request, 'blog/comments_management.html', context)

@admin_only
def full_comments(request):

    comments = Comment.objects.all().order_by('-date_commented')
    context = {'comments':comments}
    return render(request, 'blog/full_comments.html', context)

@admin_only
def full_replies(request):

    replies = Reply.objects.all().order_by('-date_replied')
    context = {'replies':replies}
    return render(request, 'blog/full_replies.html', context)

@admin_only
@csrf_exempt
def delete_comment(request, com_id):
    Comment.objects.get(id=com_id).delete()
    return redirect('comments')

@admin_only
@csrf_exempt
def delete_reply(request, rep_id):
    Reply.objects.get(id=rep_id).delete()
    return redirect('comments')

@admin_only
@csrf_exempt
def delete_comment2(request, com_id):
    Comment.objects.get(id=com_id).delete()
    return redirect('full_comments')

@admin_only
@csrf_exempt
def delete_reply2(request, rep_id):
    Reply.objects.get(id=rep_id).delete()
    return redirect('full_replies')

@admin_only
@csrf_exempt
def delete_flcomment(request, com_id):
    Comment.objects.get(id=com_id).delete()
    return redirect('fl_comments')

@admin_only
@csrf_exempt
def delete_flreply(request, rep_id):
    Reply.objects.get(id=rep_id).delete()
    return redirect('fl_replies')

@admin_only
def flaggedcomments(request):
    flagged_comments = Comment.objects.exclude(flagged=None)
    
    context = {'f_comm':flagged_comments}
    return render(request, 'blog/flagged_comments.html', context)

@admin_only
def flaggedreplies(request):
    flagged_replies = Reply.objects.exclude(flagged=None)
    
    context = {'f_rep':flagged_replies}
    return render(request, 'blog/flagged_replies.html', context)
#------------------------------------------------------------------------
# POST LIST AND DETAIL 
#------------------------------------------------------------------------
class ArticleListView(ListView):
    model = Post
    template_name = 'blog/main.html'
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 10

class PostDetailView(View):
    def get(self, request, pk, slug_text, *args, **kwargs):
        
        article = get_object_or_404(Post, id=pk, slug=slug_text)
        categories = Category.objects.all()
        related_posts = Post.objects.filter(category=article.category.first()).exclude(id=article.id)[:5]
        comments = article.comments.all()
        user = request.user
        form2 = ReplyForm(user, auto_id = False)
        form = CommentForm(user, auto_id = False)

        context = {
            'post': article,
            'form': form,
            'form2':form2,
            'com': comments,
            'cate':categories,
            'rela':related_posts
        }

        return render(request, 'blog/post_detail.html', context)

    def post(self, request, pk, slug_text, *args, **kwargs):
        article = get_object_or_404(Post, id=pk, slug=slug_text)
        user = request.user
        form2 = ReplyForm(user, auto_id = False)
        form = CommentForm(user, auto_id = False)
        if request.method == 'POST':

            if not request.POST.get('reply'):
                form = CommentForm(user, request.POST)
                print(form.data)
                
                if form.is_valid():
                    if request.user.is_authenticated:
                    
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('comment')
                        comment=Comment.objects.create(article=article, author=author, comment=content)
                        comment.save()
                        form = CommentForm(user, auto_id = False)

                    else:
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('comment')
                        comment=Comment.objects.create(article=article, name=name, email=email, comment=content)
                        comment.save()
                        form = CommentForm(user, auto_id = False)
        
        comments = article.comments.all()

        if request.user.is_authenticated:
            if not request.POST.get('reply'):
                if article.author != None:
                    if request.user != article.author.user:
                        notification = Notification.objects.create(notification_type=1, from_author=request.user.author, to_author=article.author, article=article)
        else:
            if not request.POST.get('reply'):
                if article.author != None:
                    notification = Notification.objects.create(notification_type=1, from_visitor = request.POST.get('name'), to_author=article.author, article=article)
        context = {
            'post': article,
            'form': form,
            'form2':form2,
            'com': comments,
        }
        
        
        if request.is_ajax():
            
            if not request.POST.get('reply'):
                html = render_to_string('blog/comments.html', context, request=request)
            return JsonResponse({'form': html})

        return render(request, 'blog/post_detail.html', context)

class CommentReplyView(View):
    def post(self, request, comment_pk, pk, slug_text, *args, **kwargs):
        article = Post.objects.get(id=pk, slug=slug_text)
        parent_comment = Comment.objects.get(id=comment_pk)
        comments = article.comments.all()
    
        user = request.user
        form = CommentForm(user, auto_id = False)
        form2 = ReplyForm(user, auto_id = False)


        if request.method == 'POST':
            if request.POST.get('reply'):
                form2 = ReplyForm(user, request.POST)
                print(form2.data)
                if form2.is_valid():
                    if request.user.is_authenticated:
                        comment = Comment.objects.get(id=request.POST.get('comment_id'))
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('reply')
                        reply = Reply.objects.create(comment=comment, author=author, reply=content)
                        reply.save()
                        form2 = ReplyForm(user, auto_id = False)
                
                    else:
                        comment = Comment.objects.get(id=request.POST.get('comment_id'))
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('reply')
                        reply=Reply.objects.create(comment=comment, name=name, email=email, reply=content)
                        reply.save()
                        form2 = ReplyForm(user, auto_id = False)
        
        if request.user.is_authenticated:
            if request.POST.get('reply'):
                if request.user != Comment.objects.get(id=request.POST.get('comment_id')).author.user:
                    if Comment.objects.get(id=request.POST.get('comment_id')).author != None:
                        notification = Notification.objects.create(notification_type=2, from_author=request.user.author, to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))
        else:
            if request.POST.get('reply'):
                if Comment.objects.get(id=request.POST.get('comment_id')).author:
                    notification = Notification.objects.create(notification_type=2, from_visitor = request.POST.get('name'), to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))
        context = {'form2':form2, 'form':form, 'article':article, 'com':parent_comment, 'user':user,}

        if request.is_ajax():
            if request.POST.get('reply'):
                html = render_to_string('blog/replies.html', context, request=request)
                html2 = render_to_string('blog/rep.html', context, request=request)
            return JsonResponse({'form2': html, 'form3': html2})

        return redirect(article.get_absolute_url())

class CommentFlagToggle(View):
    def post(self, request, pk, slug_text, comment_pk, *args, **kwargs):
        user = request.user
        author = user.author
        comment = Comment.objects.get(id=comment_pk)
        if request.method == 'POST':
            article = Post.objects.get(id=pk, slug=slug_text)
            comment = Comment.objects.get(id=comment_pk)
            _flagged = author in comment.flagged.all()
            if _flagged :
                comment.flagged.remove(author)
            else:
                comment.flagged.add(author)
                if comment.author != None:
                    notification = Notification.objects.create(notification_type=6, from_author=request.user.author, to_author=comment.author, comment=comment)
        
        return JsonResponse({'flagged':_flagged})

class ReplyCommentFlagToggle(View):
    def post(self, request, pk, slug_text, comment_pk, reply_pk, *args, **kwargs):
        user = request.user
        author = user.author
        if request.method == 'POST':
            article = Post.objects.get(id=pk, slug=slug_text)
            comment = Comment.objects.get(id=comment_pk)
            reply = Reply.objects.get(id=reply_pk)
            _flagged = author in reply.flagged.all()
            if _flagged :
                reply.flagged.remove(author)
            else:
                reply.flagged.add(author)
                if reply.author != None:
                    notification = Notification.objects.create(notification_type=7, from_author=request.user.author, to_author=reply.author, reply=reply)

        return JsonResponse({'reply_flagged':_flagged})

#------------------------------------------------------------------------------------------------
# ALL ARTICLE NOTIFICATIONS VIEW
#------------------------------------------------------------------------------------------------

class CommentArticleNotification(View):
    def get(self, request, notification_pk, pk, slug_text, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk)
        article = Post.objects.get(id=pk, slug=slug_text)

        notification.author_has_seen = True
        notification.save()

        return redirect("/{}/{}/#new_comment".format(article.id, article.slug))

class ReplyArticleNotification(View):
    def get(self, request, notification_pk, pk, slug_text, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, comment__isnull=False)
        article = Post.objects.get(id=pk, slug=slug_text)

        notification.author_has_seen = True
        notification.save()

        return redirect("/{}/{}/#replied-comments-{}".format(article.id, article.slug, notification.comment.id))

class CommentFlagArticleNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, pk, slug_text, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, comment__isnull=False)
        article = Post.objects.get(id=pk, slug=slug_text)

        notification.author_has_seen = True
        notification.save()

        return redirect("/{}/{}/#comment-{}".format(article.id, article.slug, notification.comment.id))

class ReplyFlagArticleNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, pk, slug_text, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, reply__isnull=False)
        article = Post.objects.get(id=pk, slug=slug_text)

        notification.author_has_seen = True
        notification.save()

        return redirect("/{}/{}/#replied-comments-{}".format(article.id, article.slug, notification.reply.comment.id))

'''
        
class CommentDisapprovalToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug_text")
        post_id = self.kwargs.get("pk")
        com_id = self.kwargs.get("comment_pk")
        print(slug)
        post_obj = get_object_or_404(Post, id=post_id, slug=slug)
        comment_obj = get_object_or_404(Comment, id=com_id)
        user = self.request.user
        author = user.author
        if user.is_authenticated:
            if author in comment_obj.disapproved.all():
                comment_obj.disapproved.remove(author)
            else:
                comment_obj.disapproved.add(author)
        return redirect(self.request.path)


def ajax_change_status(request):
    author_has_seen = request.GET.get('author_has_seen', False)
    pk = request.GET.get('pk', False)
    # first you get your Job model
    notification = Notification.objects.get(pk=pk)
    try:
        notification.author_has_seen = author_has_seen
        notification.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})
    return JsonResponse(data)

def removeNotification(request):
    notification = get_object_or_404(Notification, pk=request.GET.get('notification_pk'))
    notification.author_has_seen = not notification.author_has_seen
    notification.save()
    
    return redirect('/')

def removeNotification(request):
    obj = request.GET.get('notification_pk')
    data = {
        "id":obj
    }

    notification = Notification.objects.get(id=obj)
    if notification.author_has_seen == False:
        notification.author_has_seen = True
        notification.save()
    return JsonResponse(data)
'''

#---------------------------------------------------------------------------------------------------
# ADMIN SECTION
#------------------------------------------------------------------------------------------------

class AdminView(ListView):
    model = Author
    template_name = 'blog/admins.html'
    context_object_name = 'admins'
    queryset = Author.objects.filter(user__is_staff=True)

class AdminProfileView(View):
    def get(self, request, profile_slug, *args, **kwargs):

        admin = Author.objects.get(user__is_staff=True, slug=profile_slug)

        context = {'author':admin}

        return render(request, 'blog/admin_profile.html', context)

class AdminPostListView(ListView):
    model = Post
    template_name = 'blog/admin_articles.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        author = Author.objects.get(slug=self.kwargs.get('profile_slug'))
        return Post.objects.filter(author=author).order_by('-date_created')    


#--------------------------------------------------------------------------------------------
# PROFILE SECTION
#------------------------------------------------------------------------------------------------

class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        author = Author.objects.get(user=request.user)

        context = {'author':author}
        return render(request, 'blog/profile.html', context)    

@login_required(login_url='login')
def save_profile_form(request, form, template_name, ):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            form.save()
            data['form_is_valid'] = True
            author = request.user.author
            data['html_profile_list'] = render_to_string('blog/profile_list.html', {
                'author': author, 'user':user
            })
        else:
            data['form_is_valid'] = False

    context = {'form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)          

@login_required(login_url='login')
def profile_edit(request, pk_test):

    author = Author.objects.get(id=pk_test)
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(user, request.POST, request.FILES, instance=author,)

    else:
        form = ProfileForm(user, instance=author)

    return save_profile_form(request, form, 'blog/profile_edit.html')
#------------------------------------------------------------------------------------------------
# POSTS CATEGORY SECTION
#------------------------------------------------------------------------------------------------
category_object = None
class CategoryView(ListView):
    model = Category
    template_name = 'blog/categories.html'
    context_object_name = 'categories'

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blog/posts_category_page.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        global category_object
        category_object = Category.objects.get(slug=self.kwargs.get('cat_slug'))
        return Post.objects.filter(category=category_object).order_by('-date_created')

class CategoryQuestionListView(ListView):
    model = Question
    template_name = 'blog/questions_category_page.html'
    context_object_name = 'questions'
    paginate_by = 10

    def get_queryset(self):
#        global category_object
        question_category_object = Category.objects.get(slug=self.kwargs.get('cat_slug'))
        return Question.objects.filter(category=question_category_object).order_by('-date_created')

#---------------------------------------------------------------------------
# POST C-R-U-D SECTION
#------------------------------------------------------------------------------------------------

@admin_only
def save_post_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            
            author = Author.objects.get(user=user)
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            form.save_m2m()
            data['form_is_valid'] = True
            articles = Post.objects.all()
            admin_articles = Post.objects.filter(author=author)
            '''
            current = request.path  
            print(current)
            id_string = current.split("/")[-2]
            print(id_string)
            '''
            def get_category():
                return category_object
            #print(category)
        
            category_articles = Post.objects.filter(category=get_category())
            print(category_articles)
            
            data['html_post_list3'] = render_to_string('blog/partial_admin_articles.html', {
                'page_obj': admin_articles, 'user': user
            })

            data['html_post_list2'] = render_to_string('blog/partial_posts_category_page.html', {
                'page_obj': category_articles, 'user': user
            })
            data['html_post_list'] = render_to_string('blog/partial_post_list.html', {
                'page_obj': articles, 'user': user
            })
        else:
            data['form_is_valid'] = False

    context = {'form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)            

@admin_only
def createPost(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        for field in form:
            print("Field Error:", field.name,  field.errors)

    else:
        form = PostForm()
    return save_post_form(request, form, 'blog/partial_post_create.html')    

@admin_only
def updatePost(request, pk):
    article = get_object_or_404(Post, id=pk)
    form = PostForm(instance=article)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=article)

    return save_post_form(request, form, 'blog/partial_post_update.html')    

@admin_only
def deletePost(request, pk):
    article = get_object_or_404(Post, id=pk)
    data = dict()
    if request.method == 'POST':
        article.delete()

        data['form_is_valid'] = True
        articles = Post.objects.all()
        data['html_post_list'] = render_to_string('blog/partial_post_list.html', {'post':articles})
    else:
        context = {'post':article}
        data['html_form'] = render_to_string('blog/partial_post_delete.html', context, request=request)
    return JsonResponse(data)


#------------------------------------------------------------------------------------------------
# COMMUNITY SECTION
#------------------------------------------------------------------------------------------------
#question_object = 1
class QuestionListView(ListView):
    model = Question
    template_name = 'blog/community.html'
    context_object_name = 'questions'
    ordering = ['-date_created']
    paginate_by = 16

class QuestionDetailView(View):
    def get(self, request, question_pk, question_slug, *args, **kwargs):
 #       global question_object
        question_object = Question.objects.get(id=question_pk, slug=question_slug)
        answers = question_object.question_comments.all()
        categories = Category.objects.all()
        related_questions = Question.objects.filter(category=question_object.category.first()).exclude(id=question_object.id)[:5]

        user = request.user
        form2 = ReplyForm(user, auto_id = False)
        form = CommentForm(user, auto_id = False)

        context = {
            'question':question_object,
            'com':answers,
            'categories':categories,
            'related_questions':related_questions,
            'form':form,
            'form2':form2
        }

        return render(request, 'blog/question_detail.html', context)

    def post(self, request, question_pk, question_slug, *args, **kwargs):

        question = Question.objects.get(id=question_pk, slug=question_slug)
        user = request.user
        form2 = ReplyForm(user, auto_id = False)
        form = CommentForm(user, auto_id = False)

        if request.method == 'POST':
            
            if not request.POST.get('reply'):
                form = CommentForm(user, request.POST)
                print(form.data)
                
                if form.is_valid():
                    if request.user.is_authenticated:
                    
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('comment')
                        answer=Comment.objects.create(question=question_object, author=author, comment=content)
                        answer.save()
                        form = CommentForm(user, auto_id = False)

                    else:
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('comment')
                        answer=Comment.objects.create(question=question_object, name=name, email=email, comment=content)
                        answer.save()
                        form = CommentForm(user, auto_id = False)

        answers = question.question_comments.all()

        if request.user.is_authenticated:
            if not request.POST.get('reply'):
                if request.user != question.author.user:
                    if question.author != None:
                        notification = Notification.objects.create(notification_type=1, from_author=request.user.author, to_author=question.author, question=question)
        else:
            if not request.POST.get('reply'):
                if question.author != None:
                    notification = Notification.objects.create(notification_type=1, from_visitor = request.POST.get('name'), to_author=question.author, question=question)

        context = {
            'question':question,
            'form':form,
            'form2':form2,
            'com':answers
        }

        if request.is_ajax():
            if not request.POST.get('reply'):
                html = render_to_string('blog/comments.html', context, request=request)            
            return JsonResponse({'form': html})

        return render(request, 'blog/question_detail.html', context)

class AnswerReplyView(View):
    def post(self, request, question_pk, question_slug, answer_pk, *args, **kwargs):

        question = Question.objects.get(id=question_pk, slug=question_slug)
        user = request.user
        form2 = ReplyForm(user, auto_id = False)
        form = CommentForm(user, auto_id = False)
        parent_answer = Comment.objects.get(id=answer_pk)

        if request.method == 'POST':
            if request.POST.get('reply'):
                form2 = ReplyForm(user, request.POST)
                print(form2.data)
                if form2.is_valid():
                    if request.user.is_authenticated:
                        answer = Comment.objects.get(id=request.POST.get('comment_id'))
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('reply')
                        reply_answer = Reply.objects.create(comment=answer, author=author, reply=content)
                        reply_answer.save()
                        form2 = ReplyForm(user, auto_id = False)
                
                    else:
                        answer = Comment.objects.get(id=request.POST.get('comment_id'))
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('reply')
                        reply_answer=Reply.objects.create(comment=answer, name=name, email=email, reply=content)
                        reply_answer.save()
                        form2 = ReplyForm(user, auto_id = False)

        answers = question.question_comments.all()

        if request.user.is_authenticated:
            if request.POST.get('reply'):
                if request.user != Comment.objects.get(id=request.POST.get('comment_id')).author.user:
                    if Comment.objects.get(id=request.POST.get('comment_id')).author != None:
                        notification = Notification.objects.create(notification_type=2, from_author=request.user.author, to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))
        else:
            if request.POST.get('reply'):
                if Comment.objects.get(id=request.POST.get('comment_id')).author != None:
                    notification = Notification.objects.create(notification_type=2, from_visitor = request.POST.get('name'), to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))


        context = {
            'question':question,
            'form':form,
            'form2':form2,
            'com':parent_answer
        }

        if request.is_ajax():
            if request.POST.get('reply'):
                html = render_to_string('blog/replies.html', context, request=request)
                html2 = render_to_string('blog/rep.html', context, request=request)
            return JsonResponse({'form2': html, 'form3': html2})

        return redirect(question.get_absolute_url())

@login_required(login_url='login')
def save_question_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            author = Author.objects.get(user=user)
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            form.save_m2m()
            data['form_is_valid'] = True
            questions = Question.objects.all()
            current = request.path
            print(current)
            path_name = current.split("/")[1]
            
            if path_name == 'update_question':

  #              id = question_object.id
                question = Question.objects.get(id=form.instance.pk)
                print(question)

                data['html_question_detail'] = render_to_string('blog/partial_question_detail.html', {
                'question': question, 'user': user
                })

            data['html_question_list'] = render_to_string('blog/partial_question_list.html', {
                'questions': questions, 'user': user
            })

        else:
            data['form_is_valid'] = False

    context = {'form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@login_required(login_url='login')
def postQuestion(request):

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        for field in form:
            print("Field Error:", field.name,  field.errors)

    else:
        form = QuestionForm(auto_id = False)
    return save_question_form(request, form, 'blog/partial_question_create.html')    

@login_required(login_url='login')
def updateQuestion(request, pk):
    question = get_object_or_404(Question, id=pk)
    form = QuestionForm(instance=question, auto_id = False)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)

    return save_question_form(request, form, 'blog/partial_question_update.html')    

@login_required(login_url='login')
def deleteQuestion(request, pk):
    question = get_object_or_404(Question, id=pk)
    data = dict()
    if request.method == 'POST':
        question.delete()

        data['form_is_valid'] = True
        questions = Question.objects.all()
        data['html_question_list'] = render_to_string('blog/partial_question_list.html', {'questions':questions})
    else:
        context = {'question':question}
        data['html_form'] = render_to_string('blog/partial_question_delete.html', context, request=request)
    return JsonResponse(data)

class UserQuestionListView(ListView):
    model = Question
    template_name = 'blog/user_questions.html'
    context_object_name = 'questions'
    ordering = ['-date_created']
    paginate_by = 16

    def get_queryset(self):
        author = Author.objects.get(slug=self.kwargs.get('profile_slug'))
        return Question.objects.filter(author=author)

class QuestionCommentFlagToggle(LoginRequiredMixin, View):
    def post(self, request, question_pk, question_slug, answer_pk, *args, **kwargs):
        user = request.user
        author = user.author
        if request.method == 'POST':
            question = Question.objects.get(id=question_pk, slug=question_slug)
            answer = Comment.objects.get(id=answer_pk)
            _flagged = author in answer.flagged.all()
            if _flagged :
                answer.flagged.remove(author)
            else:
                answer.flagged.add(author)
                if answer.author != None:
                    notification = Notification.objects.create(notification_type=6, from_author=request.user.author, to_author=answer.author, comment=answer)

        return JsonResponse({'flagged':_flagged})

class QuestionReplyCommentFlagToggle(LoginRequiredMixin, View):
    def post(self, request, question_pk, question_slug, answer_pk, reply_pk, *args, **kwargs):
        user = request.user
        author = user.author
        if request.method == 'POST':
            question = Question.objects.get(id=question_pk, slug=question_slug)
            answer = Comment.objects.get(id=answer_pk)
            reply_answer = Reply.objects.get(id=reply_pk)
            _flagged = author in reply_answer.flagged.all()
            if _flagged :
                reply_answer.flagged.remove(author)
            else:
                reply_answer.flagged.add(author)
                if reply_answer.author != None:
                    notification = Notification.objects.create(notification_type=7, from_author=request.user.author, to_author=reply_answer.author, reply=reply_answer)

        return JsonResponse({'reply_flagged':_flagged})

#------------------------------------------------------------------------------------------------
# ALL QUESTION NOTIFICATIONS VIEW
#------------------------------------------------------------------------------------------------

class AnswerQuestionNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, question_pk, question_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk)
        question = Question.objects.get(id=question_pk, slug=question_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/questions/{}/{}/#new_comment".format(question.id, question.slug))

class ReplyAnswerQuestionNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, question_pk, question_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, comment__isnull=False)
        question = Question.objects.get(id=question_pk, slug=question_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/questions/{}/{}/#replied-comments-{}".format(question.id, question.slug, notification.comment.id))

class AnswerFlagQuestionNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, question_pk, question_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, comment__isnull=False)
        question = Question.objects.get(id=question_pk, slug=question_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/questions/{}/{}/#comment-{}".format(question.id, question.slug, notification.comment.id))

class ReplyAnswerFlagQuestionNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, question_pk, question_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, reply__isnull=False)
        question = Question.objects.get(id=question_pk, slug=question_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/questions/{}/{}/#replied-comments-{}".format(question.id, question.slug, notification.reply.comment.id))


#------------------------------------------------------------------------------------------------
# NEWS AND INFO
#------------------------------------------------------------------------------------------------
from django.db import transaction
#news_object = 2
class NewsListView(ListView):
    model = News
    template_name = 'blog/news.html'
    context_object_name = 'news'
    queryset = News.objects.all().order_by('-date_created')
    paginate_by = 10

class NewsDetailView(View):
    def get(self, request, news_slug, *args, **kwargs):
 #       global news_object
        news_object = News.objects.get(slug=news_slug)
        comments = news_object.news_comments.all()
        other_news = News.objects.all().exclude(id=news_object.id).order_by('-date_created')[:5]
        user = request.user
        form2 = ReplyForm(user, auto_id = False)
        form = CommentForm(user, auto_id = False)



        context = {'n_obj':news_object, 'o_news':other_news, 'com':comments, 'form':form, 'form2':form2}
        return render(request, 'blog/news_detail.html', context)

    def post(self, request, news_slug, *args, **kwargs):

        news_obj = get_object_or_404(News, slug=news_slug)
        user = request.user
        form = CommentForm(user, auto_id = False)
        form2 = ReplyForm(user, auto_id = False)
        if request.method == 'POST':
            if not request.POST.get('reply'):
                form = CommentForm(user, request.POST)
                print(form.data)
                
                if form.is_valid():
                    if request.user.is_authenticated:
                    
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('comment')
                        comment=Comment.objects.create(news=news_obj, author=author, comment=content)
                        comment.save()
                        form = CommentForm(user, auto_id = False)

                    else:
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('comment')
                        comment=Comment.objects.create(news=news_obj, name=name, email=email, comment=content)
                        comment.save()
                        form = CommentForm(user, auto_id = False)

        comments = news_object.news_comments.all()

        if request.user.is_authenticated:
            if not request.POST.get('reply'):
                if request.user != news_obj.author.user:
                    if news_obj.author != None:
                        notification = Notification.objects.create(notification_type=1, from_author=request.user.author, to_author=news_obj.author, news=news_obj)
    
        else:
            if not request.POST.get('reply'):
                if news_obj.author != None:
                    notification = Notification.objects.create(notification_type=1, from_visitor = request.POST.get('name'), to_author=news_obj.author, news=news_obj)
    
        context = {
            'n_obj': news_obj,
            'form': form,
            'form2': form2,
            'com': comments,
        }
        
        
        if request.is_ajax():
            if not request.POST.get('reply'):
                html = render_to_string('blog/comments.html', context, request=request)
            return JsonResponse({'form': html})

        return render(request, 'blog/news_detail.html', context)

class CommentReplyNewsView(View):

    def post(self, request, news_slug, comment_pk, *args, **kwargs):
        news_obj = get_object_or_404(News, slug=news_slug)
        parent_comment = Comment.objects.get(id=comment_pk)
        user = request.user
        form = CommentForm(user, auto_id = False)
        form2 = ReplyForm(user, auto_id = False)
        if request.method == 'POST':
            if request.POST.get('reply'):
                form2 = ReplyForm(user, request.POST)
                print(form2.data)
                if form2.is_valid():
                    if request.user.is_authenticated:
                        comment = Comment.objects.get(id=request.POST.get('comment_id'))
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('reply')
                        reply = Reply.objects.create(comment=comment, author=author, reply=content)
                        reply.save()
                        form2 = ReplyForm(user, auto_id = False)
                
                    else:
                        comment = Comment.objects.get(id=request.POST.get('comment_id'))
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('reply')
                        reply=Reply.objects.create(comment=comment, name=name, email=email, reply=content)
                        reply.save()
                        form2 = ReplyForm(user, auto_id = False)


        if request.user.is_authenticated:
            if request.POST.get('reply'):
                if request.user != Comment.objects.get(id=request.POST.get('comment_id')).author.user:
                    if Comment.objects.get(id=request.POST.get('comment_id')).author != None:
                        notification = Notification.objects.create(notification_type=2, from_author=request.user.author, to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))

        else:
            if request.POST.get('reply'):
                if Comment.objects.get(id=request.POST.get('comment_id')).author != None:
                    notification = Notification.objects.create(notification_type=2, from_visitor = request.POST.get('name'), to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))

        context = {
            'n_obj': news_obj,
            'form': form,
            'form2': form2,
            'com': parent_comment,
        }
        
        
        if request.is_ajax():
            if request.POST.get('reply'):
                html = render_to_string('blog/replies.html', context, request=request)
                html2 = render_to_string('blog/rep.html', context, request=request)
            return JsonResponse({'form2': html, 'form3': html2})

        return redirect(news_obj.get_absolute_url())

@admin_only
def save_news_form(request, form, template_name, ):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            author = user.author
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            data['form_is_valid'] = True
            news = News.objects.all().order_by('-date_created')
            data['html_news_list'] = render_to_string('blog/news_list.html', {
                'news': news
            })
            current = request.path
            print(current)
            path_name = current.split("/")[1]
            
            if path_name == 'update_news':

  #              id = news_object.id
                news_obj = News.objects.get(id=form.instance.pk)
                print(news_obj)
                data['n_obj_list'] = render_to_string('blog/news_object_detail.html', {
                    'n_obj': news_obj, 'user':user
                })
        else:
            data['form_is_valid'] = False

    with transaction.atomic():
        for author in Author.objects.all():
            if request.POST.get('news_num'):
                if request.user != author.user:
                    notification = Notification.objects.create(news_num=request.POST.get('news_num'), notification_type=4, title=request.POST.get('title'), text=request.POST.get('text'), to_author=author)

    context = {'form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

@admin_only
def postNews(request):

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        for field in form:
            print("Field Error:", field.name,  field.errors)

    else:
        form = NewsForm(auto_id = False)
    return save_news_form(request, form, 'blog/news_create.html')    

@admin_only
def updateNews(request, pk):
    news_object = get_object_or_404(News, id=pk)
    form = NewsForm(instance=news_object, auto_id = False)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news_object)

    return save_news_form(request, form, 'blog/news_update.html')    

@admin_only
def deleteNews(request, pk):
    news_obj = get_object_or_404(News, id=pk)
    data = dict()
    if request.method == 'POST':
        news_obj.delete()
    else:
        context = {'n_obj':news_obj}
        data['html_form'] = render_to_string('blog/news_delete.html', context, request=request)
    return JsonResponse(data)

class NewsCommentFlagToggle(LoginRequiredMixin, View):
    def post(self, request, news_slug, comment_pk, *args, **kwargs):
        user = request.user
        author = user.author
        if request.method == 'POST':
            news_obj = News.objects.get(slug=news_slug)
            comment = Comment.objects.get(id=comment_pk)
            _flagged = author in comment.flagged.all()
            if _flagged :
                comment.flagged.remove(author)
            else:
                comment.flagged.add(author)
                if comment.author != None:
                    notification = Notification.objects.create(notification_type=6, from_author=request.user.author, to_author=comment.author, comment=comment)

        return JsonResponse({'flagged':_flagged})

class NewsReplyCommentFlagToggle(LoginRequiredMixin, View):
    def post(self, request, news_slug, comment_pk, reply_pk, *args, **kwargs):
        user = request.user
        author = user.author
        if request.method == 'POST':
            news_obj = News.objects.get(slug=news_slug)
            comment = Comment.objects.get(id=comment_pk)
            reply = Reply.objects.get(id=reply_pk)
            _flagged = author in reply.flagged.all()
            if _flagged :
                reply.flagged.remove(author)
            else:
                reply.flagged.add(author)
                if reply.author != None:
                    notification = Notification.objects.create(notification_type=7, from_author=request.user.author, to_author=reply.author, reply=reply)

        return JsonResponse({'reply_flagged':_flagged})

#------------------------------------------------------------------------------------------------
# ALL NEWS NOTIFICATIONS VIEW
#------------------------------------------------------------------------------------------------

class CommentNewsNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, news_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk)
        news_obj = News.objects.get(slug=news_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/news_detail/{}/#new_comment".format(news_obj.slug))

class ReplyNewsNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, news_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, comment__isnull=False)
        news_obj = News.objects.get(slug=news_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/news_detail/{}/#replied-comments-{}".format(news_obj.slug, notification.comment.id))

class CommentFlagNewsNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, news_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, comment__isnull=False)
        news_obj = News.objects.get(slug=news_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/news_detail/{}/#comment-{}".format(news_obj.slug, notification.comment.id))

class ReplyFlagNewsNotification(LoginRequiredMixin, View):
    def get(self, request, notification_pk, news_slug, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, reply__isnull=False)
        news_obj = News.objects.get(slug=news_slug)

        notification.author_has_seen = True
        notification.save()

        return redirect("/news_detail/{}/#replied-comments-{}".format(news_obj.slug, notification.reply.comment.id))
        
class NewsInfoNotification(LoginRequiredMixin, View):
    def get(self, request, title_param, n_param, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk, to_author=request.user.author)
        news_obj = News.objects.get(title=title_param, news_num=n_param)

        notification.author_has_seen = True
        notification.save()
            

        return redirect(news_obj.get_absolute_url())

class RemoveNotification(LoginRequiredMixin, View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(id=notification_pk)

        notification.author_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')

class MarkReadView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(to_author=request.user.author).exclude(author_has_seen=True).exclude(admin_notifications__isnull=False)
        notifications.update(author_has_seen=True)
        
        return HttpResponse('Success', content_type='text/plain')

#-------------------------------------------------------------------------------------------------
# COMMENT EDIT AND DELETE
#------------------------------------------------------------------------------------------------
@login_required(login_url='login')
def save_comment_form(request, form, template_name, ):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            user = request.user
            author = user.author
            instance = form.save(commit=False)
            instance.author = author
            instance.save()
            data['form_is_valid'] = True
            
        else:
            data['form_is_valid'] = False

    context = {'form':form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)          

@login_required(login_url='login')
def comment_edit(request, comment_pk):

    comment = Comment.objects.get(id=comment_pk)
    user = request.user
    if request.method == 'POST' and request.user.author == comment.author:
        form = CommentForm(user, request.POST, instance=comment)

    else:
        form = CommentForm(user, instance=comment, auto_id = False)

    return save_comment_form(request, form, 'blog/comment_edit.html')

@login_required(login_url='login')
def comment_delete(request, comment_pk):
    comment = Comment.objects.get(id=comment_pk)
    data = dict()
    if request.method == 'POST' and request.user.author == comment.author:
        comment.delete()
        data['form_is_valid'] = True
    else:
        context = {'com':comment}
        data['html_form'] = render_to_string('blog/comment_delete.html', context, request=request)
    return JsonResponse(data)

@login_required(login_url='login')
def reply_edit(request, reply_pk):

    reply = Reply.objects.get(id=reply_pk)
    user = request.user
    if request.method == 'POST' and request.user.author == reply.author:
        form = ReplyForm(user, request.POST, instance=reply)

    else:
        form = ReplyForm(user, instance=reply, auto_id = False)

    return save_comment_form(request, form, 'blog/comment_edit.html')

@login_required(login_url='login')
def reply_delete(request, reply_pk):
    reply = Reply.objects.get(id=reply_pk)
    data = dict()
    if request.method == 'POST' and request.user.author == reply.author:
        reply.delete()
        data['form_is_valid'] = True
        data['reply_total'] = render_to_string('blog/rep.html', {'com': reply.comment}, request=request)
    else:
        context = {'r':reply}
        data['html_form'] = render_to_string('blog/comment_delete.html', context, request=request)
        
    return JsonResponse(data)

#-------------------------------------------------------------------------------------------------
# SEARCH QUERY
#------------------------------------------------------------------------------------------------
def post_search(request):
    form = PostSearchForm()
    results = []
    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = chain(Post.objects.filter(
                title__contains=search_string), Question.objects.filter(
                title__contains=search_string), Author.objects.filter(user__is_staff=True).filter(full_name__contains=search_string)) 

            data = serializers.serialize('json', list(
                search_string), fields=('id', 'title', 'slug', 'text', 'body', 'full_name'))

            return JsonResponse({'search_string': data})

    return render(request, 'blog/search.html', {'form': form, 'results': results})

#-------------------------------------------------------------------------------------------------
# ABOUT -- TERMS & CONDITIONS -- COMMUNITY STANDARDS
#-------------------------------------------------------------------------------------------------

class AboutView(View):
  def get(self, request, *args, **kwargs):
    queryset = About.objects.all()[:1]
    user=request.user
    form = ContactForm(user)
    return render(request, 'blog/about.html', {'about':queryset, 'form':form})
  
  def post(self, request, *args, **kwargs):
    queryset = About.objects.all()[:1]
    user = request.user
    form = ContactForm(user)
    if request.method == 'POST':
      form = ContactForm(user, request.POST)
      if form.is_valid():
        if request.user.is_authenticated:
          author = request.user.author
          message = request.POST.get('message')
          contact = Contact.objects.create(author=author, message=message)
          contact.save()
          sweetify.success(request, title='Success', text='Thank you for contacting us, we\'ll get back to you shortly ', icon='success', button='Ok', timer=2500)
          return redirect('about')
          
        else:
          name = request.POST.get('name')
          email = request.POST.get('email')
          message = request.POST.get('message')
          contact = Contact.objects.create(name=name, email=email, message=message)
          contact.save()
          sweetify.success(request, title='Success', text='Thank you for contacting us, we\'ll get back to you shortly ', icon='success', button='Ok', timer=2500)
          return redirect('about')
  
      else:
        sweetify.error(request, title= 'Error', text = 'Something went wrong, please try again later', icon = 'error', button = 'Ok', timer=2500)
  
    context = {'about':queryset, 'form':form}
      
    return render(request, 'blog/about.html', context)


class TermsView(ListView):
    model = Terms_And_Conditions
    template_name = 'blog/terms.html'
    queryset = Terms_And_Conditions.objects.all()
    context_object_name = 'terms'                                                                                                                                                                                       


class CommunityStandards(ListView):
    model = Community_Standards
    template_name = 'blog/community_standards.html'
    queryset = Community_Standards.objects.all()
    context_object_name = 'community_standards'

#------------------------------------------------------------------------------------------------
# USEFUL ALTERNATIVES
#------------------------------------------------------------------------------------------------

'''
def create_comment(request, pk, slug_text):
    current_date = timezone.now()
    article = get_object_or_404(Post, id=pk, slug=slug_text)
    if request.user.is_authenticated:
        author = Author.objects.get(user=request.user)
        comment = request.POST.get("comment", False)
        image = request.POST.get("image", False)
        created_obj = Comment.objects.create(author=author, date_commented=current_date, article=article, comment=comment, image=image)

    else:
        name = request.POST.get('name', False)
        email = request.POST.get('email', False)
        
        comment = request.POST.get("comment", False)
        image = request.POST.get("image", False)

        created_obj = Comment.objects.create(name=name, date_commented=current_date, article=article, email=email, comment=comment, image=image)

    return redirect(article.get_absolute_url())

def reply(request, pk, slug_text, comment_id):
    article = get_object_or_404(Post, id=pk, slug=slug_text)
    user = request.user

    form = ReplyForm(user)
    if request.method == 'POST':
        form = ReplyForm(user, request.POST)
        print(form.data)
        if form.is_valid():
            if request.user.is_authenticated:
                comment = Comment.objects.get(id=request.POST.get('comment_id'))
                author = Author.objects.get(user=request.user)
                content = request.POST.get('reply')
                reply = Reply.objects.create(comment=comment, author=author, reply=content)
                reply.save()
                form2 = ReplyForm(user)
                return redirect(article.get_absolute_url())
        
            else:
                comment = Comment.objects.get(id=request.POST.get('comment_id'))
                name = request.POST.get('name')
                email = request.POST.get('email')
                content = request.POST.get('reply')
                reply=Reply.objects.create(comment=comment, name=name, email=email, reply=content)
                reply.save()
                form2 = ReplyForm(user)
                return redirect(article.get_absolute_url())

    context = {'reply_form':form}

    if request.is_ajax():
        html = render_to_string('blog/reply.html', context, request=request)

        return JsonResponse({'reply_form': html})

    return render(request, 'blog/reply.html', context)

def home(request):

    articles = Post.objects.all().order_by('-date_created')
    paginator = Paginator(articles, 4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    context = {'articles':articles, 'cate':categories, 'page_obj':page_obj}
    return render(request, 'blog/main.html', context)

def community(request):

    questions = Question.objects.all()

    context = {'questions': questions}
    return render(request, 'blog/community.html', context)

def detail(request, pk, slug_text):
    article = get_object_or_404(Post, id=pk, slug=slug_text)

    categories = Category.objects.all()
    related_posts = Post.objects.filter(category=article.category.first()).exclude(id=article.id)[:5]
    comments = article.comments.all()

    user = request.user
    form2 = ReplyForm(user)
    form = CommentForm(user)

    if request.method == 'POST':
        try:
            if request.POST['reply']:
                form2 = ReplyForm(user, request.POST)
                print(form2.data)
                if form2.is_valid():
                    if request.user.is_authenticated:
                        comment = Comment.objects.get(id=request.POST.get('comment_id'))
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('reply')
                        reply = Reply.objects.create(comment=comment, author=author, reply=content)
                        reply.save()
                        form2 = ReplyForm(user)
                        return redirect(article.get_absolute_url())
                
                    else:
                        comment = Comment.objects.get(id=request.POST.get('comment_id'))
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('reply')
                        reply=Reply.objects.create(comment=comment, name=name, email=email, reply=content)
                        reply.save()
                        form2 = ReplyForm(user)
                        return redirect(article.get_absolute_url())
                    
        except:
            form = CommentForm(user, request.POST)
            print(form.data)
            
            if form.is_valid():
                if request.user.is_authenticated:
                
                    author = Author.objects.get(user=request.user)
                    content = request.POST.get('comment')
                    comment=Comment.objects.create(article=article, author=author, comment=content)
                    comment.save()
                    form = CommentForm(user)
                    return redirect(article.get_absolute_url())

                else:
                    name = request.POST.get('name')
                    email = request.POST.get('email')
                    content = request.POST.get('comment')
                    comment=Comment.objects.create(article=article, name=name, email=email, comment=content)
                    comment.save()
                    form = CommentForm(user)
                    return redirect(article.get_absolute_url())
            
    if request.user.is_authenticated:
        if request.POST.get('reply'):
            notification = Notification.objects.create(notification_type=2, from_author=request.user.author, to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))
        else:
            notification = Notification.objects.create(notification_type=1, from_author=request.user.author, to_author=article.author, article=article)

    else:
        if request.POST.get('reply'):
            notification = Notification.objects.create(notification_type=2, from_visitor = request.POST.get('name'), to_author=Comment.objects.get(id=request.POST.get('comment_id')).author, comment=Comment.objects.get(id=request.POST.get('comment_id')))
        else:
            notification = Notification.objects.create(notification_type=1, from_visitor = request.POST.get('name'), to_author=article.author, article=article)

    context = {'post':article, 'cate':categories, 'rela':related_posts, 'com':comments, 'form': form, 'form2':form2, 'replies':replies}
    
    if request.is_ajax():
        html = render_to_string('blog/comments.html', context, request=request)
        html2 = render_to_string('blog/replies.html', context, request=request)

        return JsonResponse({'form': html, 'form2':html2})

    return render(request, 'blog/post_detail.html', context)

def questionDetail(request, question_pk, question_slug):

    global question_object
    question_object = Question.objects.get(id=question_pk, slug=question_slug)
    answers = question_object.answers.all()
    categories = Category.objects.all()
    related_questions = Question.objects.filter(category=question_object.category.first()).exclude(id=question_object.id)[:5]

    user = request.user
    form2 = ReplyAnswerForm(user)
    form = AnswerForm(user)

    if request.method == 'POST':
        try:
            if request.POST['reply_answer']:
                form2 = ReplyAnswerForm(user, request.POST)
                print(form2.data)
                if form2.is_valid():
                    if request.user.is_authenticated:
                        answer = Answer.objects.get(id=request.POST.get('answer_id'))
                        author = Author.objects.get(user=request.user)
                        content = request.POST.get('reply_answer')
                        reply_answer = ReplyAnswer.objects.create(answer=answer, author=author, reply_answer=content)
                        reply_answer.save()
                        form2 = ReplyAnswerForm(user)
                        return redirect(question.get_absolute_url())
                
                    else:
                        answer = Answer.objects.get(id=request.POST.get('answer_id'))
                        name = request.POST.get('name')
                        email = request.POST.get('email')
                        content = request.POST.get('reply_answer')
                        reply_answer=ReplyAnswer.objects.create(answer=answer, name=name, email=email, reply_answer=content)
                        reply_answer.save()
                        form2 = ReplyAnswerForm(user)
                        return redirect(question.get_absolute_url())
                            
        except:
            form = AnswerForm(user, request.POST)
            print(form.data)
            
            if form.is_valid():
                if request.user.is_authenticated:
                
                    author = Author.objects.get(user=request.user)
                    content = request.POST.get('answer')
                    answer=Answer.objects.create(question=question_object, author=author, answer=content)
                    answer.save()
                    form = AnswerForm(user)
                    return redirect(question_object.get_absolute_url())

                else:
                    name = request.POST.get('name')
                    email = request.POST.get('email')
                    content = request.POST.get('answer')
                    answer=Answer.objects.create(question=question_object, name=name, email=email, answer=content)
                    answer.save()
                    form = AnswerForm(user)
                    return redirect(question_object.get_absolute_url())
    
    if request.user.is_authenticated:
        notification = Notification.objects.create(notification_type=4, from_author=request.user.author, to_author=Answer.objects.get(id=request.POST.get('answer_id')).author, answer=Answer.objects.get(id=request.POST.get('answer_id')))
        notification = Notification.objects.create(notification_type=3, from_author=request.user.author, to_author=question_object.author, question=question_object)
    else:
        notification = Notification.objects.create(notification_type=4, from_visitor = request.POST.get('name'), to_author=Answer.objects.get(id=request.POST.get('answer_id')).author, answer=Answer.objects.get(id=request.POST.get('answer_id')))
        notification = Notification.objects.create(notification_type=1, from_visitor = request.POST.get('name'), to_author=question_object.author, question=question_object)
    
    context = {'question':question_object, 'categories':categories, 'related_questions':related_questions, 'answers':answers, 'form2':form2, 'form':form, 'user':user}
    
    if request.is_ajax():
        html = render_to_string('blog/answers.html', context, request=request)
        html2 = render_to_string('blog/answer_replies.html', context, request=request)

        return JsonResponse({'form': html, 'form2':html2})


    return render(request, 'blog/question_detail.html', context)

def profile(request, profile_slug):
    author = Author.objects.get(slug=profile_slug)
    
    context = {'author':author}

    return render(request, 'blog/profile.html', context)

def categories(request):

    categories = Category.objects.all()


    context = {'categories':categories}
    return render(request, 'blog/categories.html', context)

def admin_articles(request, profile_slug):
    author = Author.objects.get(slug=profile_slug)
    articles = Post.objects.filter(author=author)

    context = {'page_obj':articles}
    return render(request, 'blog/admin_articles.html', context)    

def category_page(request, cat_slug):

    global category_object 
    category_object = Category.objects.get(slug=cat_slug)
    articles = Post.objects.filter(category=category_object)

    context = {'page_obj':articles}
    return render(request, 'blog/posts_category_page.html', context)

def admins(request):

    admins = Author.objects.filter(user__is_staff=True)

    context = {'admins':admins}

    return render(request, 'blog/admins.html', context)

'''
