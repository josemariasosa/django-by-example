from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 post in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'page': page}
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    search_params = {
        'slug': post,
        'status': 'published',
        'publish__year': year,
        'publish__month': month,
        'publish__day': day
    }
    post = get_object_or_404(Post, **search_params)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to db yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the db
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'post': post, 'comments': comments,
               'new_comment': new_comment, 'comment_form': comment_form}
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = ''.join([f"Read {post.title} at {post_url}\n\n",
                               f"{cd['name']}\' comments: {cd['comments']}"])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context)

