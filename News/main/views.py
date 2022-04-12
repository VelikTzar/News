from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.management import call_command
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, FormView, UpdateView

from .forms import ProfileForm
from .management.startscrapy import scrape

from .models import Article, Profile


# connect scrapyd service

# class HomeView(TemplateView):
#    template_name = "main/index.html"

# def scrape(request):
#
#   call_scrapy_spider()
#  print("kill me")
# return redirect('index')

class HomeView(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 12
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
    form = ProfileForm()
    model = Profile
    fields = ['first_name', 'last_name', 'date_of_birth', 'image']
    template_name = "main/profile_edit.html"








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
    #scrape()
    return redirect('index')
