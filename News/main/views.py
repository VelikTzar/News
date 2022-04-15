from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, TemplateView
from guardian.decorators import permission_required_or_403
from guardian.mixins import PermissionRequiredMixin
from guardian.shortcuts import assign_perm

from .forms import CommentForm, CommentEditForm, CommentDeleteForm
from .models import Article, Profile, Comment
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


class ArticleLikeView(LoginRequiredMixin, View):
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


class ArticleDislikeView(LoginRequiredMixin, View):
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


class ArticleSaveView(LoginRequiredMixin, View):
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


class SavedArticlesView(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 25
    template_name = "main/saved_articles.html"
    queryset = Article.objects.all().order_by('-date_published')

    def get_context_data(self, **kwargs):
        profile_id = self.request.user.pk
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.get(pk=profile_id)
        return context


class ProfileEditView(PermissionRequiredMixin, UpdateView):
    permission_required = 'main.change_profile'
    raise_exception = True
    model = Profile
    fields = ['first_name', 'last_name', 'date_of_birth', 'profile_image']
    template_name = "main/profile_edit.html"
    success_url = reverse_lazy("profile")



class ProfileDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'accounts.delete_newsuser'
    raise_exception = True
    model = NewsUser
    success_url = reverse_lazy('home no login')
    template_name = "main/profile_delete.html"


class HomeNoLoginView(TemplateView):
    template_name = "main/home_no_login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            last_article = Article.objects.latest("date_published")
            context["object"] = last_article
            return context
        except:
            context["object"] = Article(title="Title")
            return context



class SubmitCommentView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = "main/comment.html"

    def get_success_url(self):
        pk = self.kwargs.get("pk")
        return f"http://localhost:8000/article/{pk}"

    def form_valid(self, form):
        profile_id = self.request.user.pk
        profile = Profile.objects.get(pk=profile_id)
        article = Article.objects.get(pk=self.kwargs.get("pk"))
        user = self.request.user
        form.instance.user = profile
        form.instance.article = article
        super(SubmitCommentView, self).form_valid(form)
        comment = form.instance
        assign_perm('change_comment', user, comment)
        assign_perm('delete_comment', user, comment)
        assign_perm('view_comment', user, comment)
        return redirect(self.get_success_url())


class CommentLikeView(LoginRequiredMixin, View):
    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        pk = comment.article_id
        return f'http://localhost:8000/article/{pk}'

    def get(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        profile_id = self.request.user.pk
        profile = Profile.objects.get(pk=profile_id)
        if profile in comment.liked_by.all():
            comment.liked_by.remove(profile)
        else:
            if profile in comment.disliked_by.all():
                comment.disliked_by.remove(profile)
            comment.liked_by.add(profile)
        return redirect(self.get_success_url())


class CommentDislikeView(LoginRequiredMixin, View):
    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        pk = comment.article_id
        return f'http://localhost:8000/article/{pk}'

    def get(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        profile_id = self.request.user.pk
        profile = Profile.objects.get(pk=profile_id)
        if profile in comment.disliked_by.all():
            comment.disliked_by.remove(profile)
        else:
            if profile in comment.liked_by.all():
                comment.liked_by.remove(profile)
            comment.disliked_by.add(profile)
        return redirect(self.get_success_url())


@login_required
def edit_comment_view(request, pk):
    profile = Profile.objects.get(pk=request.user.pk)
    user=request.user
    comment = Comment.objects.get(pk=pk)
    if not user.has_perm('main.delete_comment', comment):
        raise PermissionDenied()
    form = CommentEditForm(instance=comment)
    if request.method == 'GET':
        context = {
            'profile': profile,
            'form': form
        }
        return render(request, 'main/edit_comment.html', context)
    else:
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            album = form.save()
            album.save()
            pk = comment.article_id
            return redirect(f"http://localhost:8000/article/{pk}")
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'main/edit_comment.html', context)



@login_required
def delete_comment_view(request, pk):
    profile = Profile.objects.get(pk=request.user.pk)
    user=request.user
    comment = Comment.objects.get(pk=pk)
    if not user.has_perm('main.delete_comment', comment):
        raise PermissionDenied()
    form = CommentDeleteForm(instance=comment)
    if request.method == 'GET':
        context = {
            'form': form,
        }
        return render(request, 'main/delete_comment.html', context)
    else:
        comment.delete()
        pk = comment.article_id
        return redirect(f"http://localhost:8000/article/{pk}")


@login_required
def ProfileDetailView(request):
    profile_pk = request.user.pk
    profile = Profile.objects.get(pk=profile_pk)
    context = {
        'profile': profile
    }
    return render(request=request, context=context, template_name="main/profile_details.html")


@user_passes_test(lambda u: u.is_superuser)
def scrape_view(request):
    scrape()
    return redirect('index')
