from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from .models import Article, Profile
from .runspider import scrape

# connect scrapyd service

# class HomeView(TemplateView):
#    template_name = "main/index.html"

# def scrape(request):
#
#   call_scrapy_spider()
#  print("kill me")
# return redirect('index')
from ..accounts.models import NewsUser


class HomeView(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 40
    queryset = Article.objects.order_by('-date_published')
    template_name = "main/index.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "main/article_details.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        profile_id = self.request.user.pk
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=profile_id)
        return context


class ArticleFullTextView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = "main/article_full_text.html"
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        profile_id = self.request.user.pk
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=profile_id)
        return context


@method_decorator(login_required, name='dispatch')
class ArticleLikeView(View):
    def get_success_url(self):
        return f'http://localhost:8000/article/{self.kwargs.get("pk")}'

    def get(self, request, *args, **kwargs):
        profile_id = self.request.user.pk
        profile = Profile.objects.get(pk=profile_id)
        article = Article.objects.get(pk=self.kwargs.get("pk"))
        if profile in article.liked_by.all():
            article.liked_by.remove(profile)
        else:
            if profile in article.disliked_by.all():
                article.disliked_by.remove(profile)
            article.liked_by.add(profile)
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class ArticleDislikeView(View):
    def get_success_url(self):
        return f'http://localhost:8000/article/{self.kwargs.get("pk")}'

    def get(self, request, *args, **kwargs):
        profile_id = self.request.user.pk
        profile = Profile.objects.get(pk=profile_id)
        article = Article.objects.get(pk=self.kwargs.get("pk"))
        if profile in article.disliked_by.all():
            article.disliked_by.remove(profile)
        else:
            if profile in article.liked_by.all():
                article.liked_by.remove(profile)
            article.disliked_by.add(profile)
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class ArticleSaveView(View):
    def get_success_url(self):
        return f'http://localhost:8000/article/{self.kwargs.get("pk")}'

    def get(self, request, *args, **kwargs):
        profile_id = self.request.user.pk
        profile = Profile.objects.get(pk=profile_id)
        article = Article.objects.get(pk=self.kwargs.get("pk"))
        if profile in article.saved_by.all():
            article.saved_by.remove(profile)
        else:
            article.saved_by.add(profile)
        return redirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class SavedArticlesView(ListView):
    model = Article
    paginate_by = 25
    template_name = "main/saved_articles.html"
    queryset = Article.objects.all().order_by('-date_published')

    def get_context_data(self, **kwargs):
        profile_id = self.request.user.pk
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=profile_id)
        return context


class ProfileEditView(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'date_of_birth', 'profile_image']
    template_name = "main/profile_edit.html"
    success_url = reverse_lazy("profile")


class ProfileDeleteView(DeleteView):
    model = NewsUser
    success_url = reverse_lazy('home no login')
    template_name = "main/profile_delete.html"


class ArticleCreateView(CreateView):
    model = Article


class ArticleEditView(UpdateView):
    model = Article


class ArticleDeleteView(DeleteView):
    model = Article


class HomeNoLoginView(TemplateView):
    template_name = "main/home_no_login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_article = Article.objects.latest("date_published")
        context["object"] = last_article
        return context


@login_required
def ProfileDetailView(request):
    profile_pk = request.user.pk
    profile = Profile.objects.get(pk=profile_pk)
    context = {
        'profile': profile
    }
    return render(request=request, context=context, template_name="main/profile_details.html")


@login_required
def scrape_view(request):
    scrape()
    return redirect('index')

