from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Profile, Follow, Notification

def home(request):
    return render(request, "core/home.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "core/register.html",
                {"error": "Username already exists"}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("dashboard")

    return render(request, "core/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "core/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "core/login.html")


@login_required
def dashboard(request):
    posts = Post.objects.all().order_by("-created_at")

    users = User.objects.exclude(
        id=request.user.id
    ).order_by("username")[:5]

    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list("following_id", flat=True)

    unread_notifications = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "core/dashboard.html",
        {
            "posts": posts,
            "users": users,
            "following_ids": following_ids,
            "unread_notifications": unread_notifications,
        }
    )

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")

        if content or image:
            Post.objects.create(
                author=request.user,
                content=content,
                image=image
            )

    return redirect("dashboard")

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

        # Create notification
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                sender=request.user,
                message=f"{request.user.username} liked your post."
            )

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content", "").strip()

        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )

            # Create notification
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    sender=request.user,
                    message=f"{request.user.username} commented on your post."
                )

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    posts = Post.objects.filter(
        author=request.user
    ).order_by("-created_at")

    followers_count = Follow.objects.filter(
        following=request.user
    ).count()

    following_count = Follow.objects.filter(
        follower=request.user
    ).count()

    return render(
        request,
        "core/profile.html",
        {
            "profile": profile,
            "posts": posts,
            "followers_count": followers_count,
            "following_count": following_count,
        }
    )
@login_required
def user_profile(request, user_id):
    target_user = User.objects.get(id=user_id)

    profile, created = Profile.objects.get_or_create(
        user=target_user
    )

    posts = Post.objects.filter(
        author=target_user
    ).order_by("-created_at")

    followers_count = Follow.objects.filter(
        following=target_user
    ).count()

    following_count = Follow.objects.filter(
        follower=target_user
    ).count()

    is_following = Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).exists()

    return render(
        request,
        "core/user_profile.html",
        {
            "target_user": target_user,
            "profile": profile,
            "posts": posts,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following,
        }
    )
@login_required
def follow_user(request, user_id):
    target_user = User.objects.get(id=user_id)

    if target_user == request.user:
        return redirect("profile")

    follow = Follow.objects.filter(
        follower=request.user,
        following=target_user
    ).first()

    if follow:
        # Unfollow
        follow.delete()

    else:
        # Follow
        Follow.objects.create(
            follower=request.user,
            following=target_user
        )

        # Create notification
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            message=f"{request.user.username} started following you."
        )

    next_page = request.GET.get("next")

    if next_page == "dashboard":
        return redirect("dashboard")

    return redirect("profile")

    return redirect("profile")
@login_required
def explore(request):
    users = User.objects.exclude(
        id=request.user.id
    ).order_by("username")

    following_ids = Follow.objects.filter(
        follower=request.user
    ).values_list("following_id", flat=True)

    user_data = []

    for user in users:
        profile, created = Profile.objects.get_or_create(
            user=user
        )

        followers_count = Follow.objects.filter(
            following=user
        ).count()

        following_count = Follow.objects.filter(
            follower=user
        ).count()

        user_data.append({
            "user": user,
            "profile": profile,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": user.id in following_ids,
        })

    return render(
        request,
        "core/explore.html",
        {
            "user_data": user_data,
        }
    )
@login_required
def notifications(request):
    notification_list = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    unread_count = Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).count()

    return render(
        request,
        "core/notifications.html",
        {
            "notifications": notification_list,
            "unread_count": unread_count,
        }
    )
@login_required
def mark_notifications_read(request):
    if request.method == "POST":
        Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(is_read=True)

    return redirect("notifications")
@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        bio = request.POST.get("bio", "").strip()

        # Update username
        if username:
            request.user.username = username

        # Update email
        request.user.email = email

        # Update bio
        profile.bio = bio

        # Update profile picture
        if request.FILES.get("profile_picture"):
            profile.profile_picture = request.FILES["profile_picture"]

        request.user.save()
        profile.save()

        return redirect("profile")

    return render(
        request,
        "core/edit_profile.html",
        {
            "profile": profile
        }
    )