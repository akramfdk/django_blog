from django.shortcuts import render, get_object_or_404
from datetime import date

from .models import Post

from django.views.generic import ListView, DetailView

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



class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["post_tags"] = self.object.tags.all()
        return context

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