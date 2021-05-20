from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post
from taggit.models import Tag
from django.db.models import Count


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self, **kwargs):
        return Post.objects.all().filter(status='published')


class PostListViewByTag(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self, **kwargs):
        tag_slug = self.kwargs["tag"] if "tag" in self.kwargs else None

        tag = get_object_or_404(Tag, slug=tag_slug)

        return Post.objects.all().filter(tags__in=[tag], status='published')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # we have a guarantee that "object" exists in context
        post = context["object"]

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tags__in=post_tags_ids, status='published')\
                                    .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                     .order_by('-same_tags','-publish')[:4]

        context["similar_posts"] = similar_posts
        return context


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def projects(request):
    return render(request, 'blog/projects.html')

# def experience(request):
#     return render(request, 'blog/experience.html')