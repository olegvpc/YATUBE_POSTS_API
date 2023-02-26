from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AvatarForm, CommentForm, PostForm, UserEditForm
from .models import Avatar, Follow, Group, Post, User


def get_paginator_page(request, data):
    page_paginator = Paginator(data, settings.PAGE_CONSTANT)
    page_number = request.GET.get("page")
    page = page_paginator.get_page(page_number)
    return page


def index(request):
    all_posts = Post.objects.all()
    page = get_paginator_page(request, all_posts)
    return render(request, 'posts/index.html', {"page": page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    all_group_posts = group.posts.all()
    page = get_paginator_page(request, all_group_posts)
    return render(request, "posts/group.html", {"group": group,
                  "page": page})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    user_avat = Avatar.objects.all()
    author_posts = author.posts.all()
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user, author=author).exists()
    page = get_paginator_page(request, author_posts)
    return render(request, "posts/profile.html", {"author": author,
                  "page": page, "following": following,
                  "user_avat": user_avat})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id, author__username=username)
    user_avat = Avatar.objects.all()
    form = CommentForm()
    return render(request, "posts/post.html", {"post": post,
                                               "form": form,
                                               "user_avat": user_avat})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")
    return render(request, "posts/new_edit_post.html",
                  {"form": form, "new_post": True})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id,
                             author__username=username)
    if request.user != post.author:
        return redirect("post", username=username, post_id=post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form.save()
        return redirect("post", username=username, post_id=post.id)
    return render(request, "posts/new_edit_post.html", {"form": form,
                                                        "post": post,
                                                        "new_post": False})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect("post", username=username, post_id=post.id)
    return render(request, "posts/post.html", {"form": form,
                                               "post": post})


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    page = get_paginator_page(request, posts)
    return render(request, "posts/follow.html", {"page": page})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect("profile", username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect("profile", username)


@login_required
def avatar_edit(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        return redirect("index")
    if Avatar.objects.filter(user_id=author.id).exists():
        user_avatar = Avatar.objects.get(user_id=author.id)
        form_avatar = AvatarForm(request.POST or None,
                                 files=request.FILES or None,
                                 instance=user_avatar)
    else:
        form_avatar = AvatarForm(request.POST, files=request.FILES or None)
    form_user = UserEditForm(request.POST or None, instance=author)
    if form_user.is_valid() and form_avatar.is_valid():
        user = form_user.save(commit=False)
        user.user_id = author.id
        user.save()
        avatar = form_avatar.save(commit=False)
        avatar.user_id = author.id
        avatar.save()
        return redirect("index")
    return render(request, "posts/avatar_edit.html",
                  {"form_user": form_user, "form_avatar": form_avatar})


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
