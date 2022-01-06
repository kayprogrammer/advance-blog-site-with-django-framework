from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------ REGISTER-- LOGIN-- RESET-- PROFILE----------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('activate-user/<uidb64>/<token>', views.activate_user, name="activate"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="blog/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="blog/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="blog/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="blog/password_reset_done.html"), name="password_reset_complete"),

    path('profile/<slug:profile_slug>/', views.ProfileView.as_view(), name="profile"), 
    path('edit_profile/<str:pk_test>/', views.profile_edit, name="update-profile"),

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------ ADMIN AREA---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    path('admins/', views.AdminView.as_view(), name="admins"),
    path('admin/<slug:profile_slug>/', views.AdminProfileView.as_view(), name="admin"),
    path('admin/<slug:profile_slug>/articles', views.AdminPostListView.as_view(), name='admin_articles'),

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------ ARTICLES AREA---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    path('', views.ArticleListView.as_view(), name='home'),
    path('<int:pk>/<slug:slug_text>/', views.PostDetailView.as_view(), name='post_detail'),

    # ARTICLE COMMENT REPLY AND FLAG NOTIFICATION
    path('notification/<int:notification_pk>/article/<int:pk>/<slug:slug_text>/', views.CommentArticleNotification.as_view(), name='post-notification'),
    path('notification/<int:notification_pk>/article/<int:pk>/<slug:slug_text>/reply/', views.ReplyArticleNotification.as_view(), name='reply-comment-post-notification'),
    path('notification/<int:notification_pk>/article/<int:pk>/<slug:slug_text>/flag/', views.CommentFlagArticleNotification.as_view(), name='flag-comment-post-notification'),
    path('notification/<int:notification_pk>/article/<int:pk>/<slug:slug_text>/reply/flag', views.ReplyFlagArticleNotification.as_view(), name='flag-reply-post-notification'),

    # ARTICLE COMMENT REPLY FLAG
    path('<int:pk>/<slug:slug_text>/comment/<int:comment_pk>/reply', views.CommentReplyView.as_view(), name='comment-reply'),
    path('<int:pk>/<slug:slug_text>/comment/<int:comment_pk>/flag', views.CommentFlagToggle.as_view(), name='flag-comment-toggle'),
    path('<int:pk>/<slug:slug_text>/comment/<int:comment_pk>/reply/<int:reply_pk>/flag', views.ReplyCommentFlagToggle.as_view(), name='flag-reply-toggle'),

    # ARTICLE CRUD
    path('create_post/', views.createPost, name="create_post"),
    path('update_post/<int:pk>/', views.updatePost, name="update_post"),
    path('delete_post/<str:pk>/', views.deletePost, name="delete_post"),
    # ARTICLE CATEGORY
    path('categories/', views.CategoryView.as_view(), name="categories"),
    path('categories/<slug:cat_slug>/', views.CategoryPostListView.as_view(), name="category_posts"),

    path('edit_comment/<str:comment_pk>/', views.comment_edit, name="edit_comment"),
    path('edit_reply/<str:reply_pk>/', views.reply_edit, name="edit_reply"),
    path('delete_comment/<str:comment_pk>/', views.comment_delete, name="delete_comment"),
    path('delete_reply/<str:reply_pk>/', views.reply_delete, name="delete_reply"),

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------ COMMUNITY AREA---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    path('community/', views.QuestionListView.as_view(), name='community'),
    path('questions/<int:question_pk>/<slug:question_slug>/', views.QuestionDetailView.as_view(), name="question_detail"),
    path('<slug:profile_slug>/questions/', views.UserQuestionListView.as_view(), name="user_questions"),
    path('question_categories/<slug:cat_slug>/', views.CategoryQuestionListView.as_view(), name="category_questions"),

    # QUESTION COMMENT REPLY FLAG NOTIFICATION
    path('notification/<int:notification_pk>/question/<int:question_pk>/<slug:question_slug>/', views.AnswerQuestionNotification.as_view(), name='question-notification'),
    path('notification/<int:notification_pk>/question/<int:question_pk>/<slug:question_slug>/reply/', views.ReplyAnswerQuestionNotification.as_view(), name='reply-answer-question-notification'),
    path('notification/<int:notification_pk>/question/<int:question_pk>/<slug:question_slug>/flag/', views.AnswerFlagQuestionNotification.as_view(), name='flag-answer-question-notification'),
    path('notification/<int:notification_pk>/question/<int:question_pk>/<slug:question_slug>/reply/flag', views.ReplyAnswerFlagQuestionNotification.as_view(), name='flag-reply-answer-question-notification'),

    # ANSWER REPLY FLAG
    path('questions/<int:question_pk>/<slug:question_slug>/answer/<int:answer_pk>/answer_reply', views.AnswerReplyView.as_view(), name="answer-reply"),
    path('questions/<int:question_pk>/<slug:question_slug>/answer/<int:answer_pk>/flag', views.QuestionCommentFlagToggle.as_view(), name='flag-question-comment-toggle'),
    path('questions/<int:question_pk>/<slug:question_slug>/answer/<int:answer_pk>/reply/<int:reply_pk>/flag', views.QuestionReplyCommentFlagToggle.as_view(), name='flag-reply-question-comment-toggle'),

    # QUESTION CRUD
    path('create_question/', views.postQuestion, name="create_question"),
    path('update_question/<int:pk>/', views.updateQuestion, name="update_question"),
    path('delete_question/<str:pk>/', views.deleteQuestion, name="delete_question"),

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------ NEWS AND INFO AREA---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    path('news_&_info/', views.NewsListView.as_view(), name="news"),
    path('news_detail/<slug:news_slug>/', views.NewsDetailView.as_view(), name="news_detail"),

    # NEWS CRUD
    path('create_news/', views.postNews, name="create_news"),
    path('update_news/<int:pk>/', views.updateNews, name="update_news"),
    path('delete_news/<str:pk>/', views.deleteNews, name="delete_news"),

    # NEWS COMMENT REPLY FLAG
    path('news_detail/<slug:news_slug>/comment/<int:comment_pk>/reply', views.CommentReplyNewsView.as_view(), name='news-comment-reply'),
    path('news_detail/<slug:news_slug>/comment/<int:comment_pk>/flag', views.NewsCommentFlagToggle.as_view(), name='flag-news-comment-toggle'),    
    path('news_detail/<slug:news_slug>/comment/<int:comment_pk>/reply/<int:reply_pk>/flag', views.NewsReplyCommentFlagToggle.as_view(), name='flag-reply-news-comment-toggle'),


    # NEWS NOTIFICATION
    path('notification/<int:notification_pk>/news/<slug:news_slug>/', views.CommentNewsNotification.as_view(), name='news-notification'),
    path('notification/<int:notification_pk>/news/<slug:news_slug>/reply/', views.ReplyNewsNotification.as_view(), name='reply-comment-news-notification'),
    path('notification/<int:notification_pk>/news/<slug:news_slug>/flag/', views.CommentFlagNewsNotification.as_view(), name='flag-comment-news-notification'),
    path('notification/<int:notification_pk>/news/<slug:news_slug>/reply/flag', views.ReplyFlagNewsNotification.as_view(), name='flag-reply-news-notification'),

    path('notification/<int:notification_pk>/news_detail/<int:n_param>/<str:title_param>/', views.NewsInfoNotification.as_view(), name='news-notification2'),

#-----------------------------------------------------------------------------------------------------------------------------------------
#-------------- COMMENTS & REPLIES MANAGEMENT -----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------
    path('comments/', views.comments_management, name="comments"),
    path('full_comments/', views.full_comments, name="full_comments"),
    path('full_replies/', views.full_replies, name="full_replies"),
    path('flagged_comments/', views.flaggedcomments, name="fl_comments"),
    path('flagged_replies/', views.flaggedreplies, name="fl_replies"),
    path('del_comment/<int:com_id>/', views.delete_comment, name="del_comment"),
    path('del_reply/<int:rep_id>/', views.delete_reply, name="del_reply"),
    path('del_comment2/<int:com_id>/', views.delete_comment2, name="del_comment2"),
    path('del_reply2/<int:rep_id>/', views.delete_reply2, name="del_reply2"),
    path('del_flcomment/<int:com_id>/', views.delete_flcomment, name="del_flcomment"),
    path('del_flreply/<int:rep_id>/', views.delete_flreply, name="del_flreply"),

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------ OTHERS----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    path('notification/mark_all_as_read/', views.MarkReadView.as_view(), name="mark_read"),
    path('notification/delete/<int:notification_pk>', views.RemoveNotification.as_view(), name='notification-delete'),

    path('about_us/', views.AboutView.as_view(), name="about"),
    path('search/', views.post_search, name='post_search'),

    path('terms_&_conditions', views.TermsView.as_view(), name="terms"),
    path('community_standards', views.CommunityStandards.as_view(), name="comm")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
]
'''
USEFUL ALTERNATIVES

path('<int:pk>/<slug:slug_text>/<str:comment_id>/reply', views.detail, name = "reply")
path('community/', views.community, name="community"),
path('<int:pk>/<slug:slug_text>/create_comment/', views.create_comment)
path('', views.home, name="home"),
path('<int:pk>/<slug:slug_text>/', views.detail, name="post_detail"),
path('profile/<slug:profile_slug>/', views.profile, name="profile"), 
path('admin_articles/<slug:profile_slug>/', views.admin_articles, name="admin_articles"),
path('categories/', views.categories, name="categories"),
path('categories/<slug:cat_slug>/', views.category_page, name="category_posts"),
path('questions/<int:question_pk>/<slug:question_slug>/', views.questionDetail, name="question_detail"),    
path('notification/delete/', views.removeNotification, name='notification-delete'),
'''