from django.urls import path
from .views import *


urlpatterns = [
    path("home/", HomeView.as_view(), name="index"),
    path("article/<int:pk>", ArticleDetailView.as_view(), name="article details"),
    path("profile/", ProfileDetailView, name="profile"),
    path("article/like/<int:pk>", ArticleLikeView.as_view(), name="like article"),
    path("article/dislike/<int:pk>", ArticleDislikeView.as_view(), name="dislike article"),
    path("article/save/<int:pk>", ArticleSaveView.as_view(), name="save article"),
    path("saved_articles/", SavedArticlesView.as_view(), name="saved articles"),
    path("scrape/", scrape_view, name="scrape"),
    path("profile/edit/<int:pk>", ProfileEditView.as_view(), name=" edit profile"),
]