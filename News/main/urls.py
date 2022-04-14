from django.urls import path
from .views import *


urlpatterns = [
    path("home/", HomeView.as_view(), name="index"),
    path("", HomeNoLoginView.as_view(), name="home no login"),

    path("profile/", ProfileDetailView, name="profile"),
    path("profile/edit/<int:pk>", ProfileEditView.as_view(), name="edit profile"),
    path("profile/delete/<int:pk>", ProfileDeleteView.as_view(), name="delete profile"),

    path("article/<int:pk>", ArticleDetailView.as_view(), name="article details"),
    path("article/full/<int:pk>", ArticleFullTextView.as_view(), name="article full"),
    path("article/like/<int:pk>", ArticleLikeView.as_view(), name="like article"),
    path("article/dislike/<int:pk>", ArticleDislikeView.as_view(), name="dislike article"),
    path("article/save/<int:pk>", ArticleSaveView.as_view(), name="save article"),
    path("article/create/<int:pk>", ArticleCreateView.as_view(), name="create article"),
    path("article/edit/<int:pk>", ArticleEditView.as_view(), name="edit article"),
    path("article/delete/<int:pk>", ArticleDeleteView.as_view(), name="delete article"),
    path("saved_articles/", SavedArticlesView.as_view(), name="saved articles"),

    path("scrape/", scrape_view, name="scrape"),

]