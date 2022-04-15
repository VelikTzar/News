from django.urls import path
from .views import *


urlpatterns = [
    path("home/", HomeView.as_view(), name="index"),
    path("", HomeNoLoginView.as_view(), name="home no login"),

    path("profile/", ProfileDetailView, name="profile"),
    path("profile/edit/<int:pk>", ProfileEditView.as_view(), name="edit profile"),
    path("profile/delete/<int:pk>", ProfileDeleteView.as_view(), name="delete profile"),

    path("article/<int:pk>", ArticleDetailView.as_view(), name="article details"),
    path("article/comment/<int:pk>", SubmitCommentView.as_view(), name="submit comment"),
    path("comment/edit/<int:pk>", edit_comment_view, name="edit comment"),
    path("comment/delete/<int:pk>", delete_comment_view, name="delete comment"),
    path("comment/like/<int:pk>", CommentLikeView.as_view(), name="like comment"),
    path("comment/dislike/<int:pk>", CommentDislikeView.as_view(), name="delete comment"),
    path("article/full/<int:pk>", ArticleFullTextView.as_view(), name="article full"),
    path("article/like/<int:pk>", ArticleLikeView.as_view(), name="like article"),
    path("article/dislike/<int:pk>", ArticleDislikeView.as_view(), name="dislike article"),
    path("article/save/<int:pk>", ArticleSaveView.as_view(), name="save article"),
    path("saved_articles/", SavedArticlesView.as_view(), name="saved articles"),


    path("scrape/", scrape_view, name="scrape"),

]