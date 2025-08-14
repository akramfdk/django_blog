from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date

from .models import Post

from django.views.generic import ListView
from django.views import View
from .forms import CommentForm

# Create your views here.
class StartingPageView(ListView):
    model = Post
    template_name = "blog/index.html"
    ordering = ["-date"]
    context_object_name = "latest_posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    model = Post
    template_name = "blog/all-posts.html"
    ordering = ["-date"]
    context_object_name = "all_posts"



class PostDetailView(View):
    # model = Post
    # template_name = "blog/post-detail.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["post_tags"] = self.object.tags.all()
    #     context["comment_form"] = CommentForm()
    #     return context

    def is_stored_post(self, request, post_id):

        stored_posts = request.session.get("stored_posts")
        is_saved_for_later = False
        if stored_posts and post_id in stored_posts:
            is_saved_for_later = True

        return is_saved_for_later
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context={
                "post": post,
                "post_tags": post.tags.all(),
                "comment_form": CommentForm(),
                "comments": post.comments.all().order_by("-id"),
                "saved_for_later": self.is_stored_post(request, post.id),
            }

        return render(request, "blog/post-detail.html", context) 

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        context={
                "post": post,
                "post_tags": post.tags.all(),
                "comment_form": comment_form,
                "comments": post.comments.all().order_by("-id"),
                "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, "blog/post-detail.html", context)
    

class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if not stored_posts:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)



    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if not stored_posts:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")

    # slug_field = "slug"
    # slug_url_kwarg = "slug"

# def post_detail(request, slug):
#     # req_post = None
#     # for post in posts:
#     #     if slug == post["slug"]:
#     #         req_post = post

#     req_post = get_object_or_404(Post, slug=slug)
#     # req_post = next(post for post in posts if post['slug'] == slug)
#     return render(request, "blog/post-detail.html", context={
#         "post": req_post,
#         "post_tags": req_post.tags.all()
#     })