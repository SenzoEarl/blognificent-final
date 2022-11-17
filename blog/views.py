from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import *
from taggit.models import Tag

from blog.forms import *
from blog.models import *
from django.db.models import Count


# Create your views here.
class Index(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'index.html'


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range, deliver the last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/list.html', {'posts': posts, 'tag': tag})


# class PostDetail(DetailView):
#     template_name = 'blog/detail.html'
#     model = Post
#     slug_field = 'slug'
#     slug_url_kwarg = 'post'

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED, slug=post,
                             publish__year=year, publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for comments
    form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    cont = {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts}
    return render(request, 'blog/detail.html', cont)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends that you read the post:{post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}`s comments: {cd['comment']}"
            # send email
            send_mail(subject, message, 'senzo.e.maseko@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailForm()
    return render(request, 'blog/share-post.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the commit
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request,
                  'blog/comment.html',
                  {'post': post, 'form': form, 'comment': comment})
