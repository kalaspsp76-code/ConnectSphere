from django.contrib import admin
from django.urls import path

from core.views import (
    home,
    dashboard,
    create_post,
    like_post,
    add_comment,
    profile,
    edit_profile,
    follow_user,
    explore,
    notifications,
    user_profile,
    mark_notifications_read,
)

from accounts.views import (
    register,
    login_view,
    logout_view,
)


urlpatterns = [

    # Admin
    path("admin/", admin.site.urls),

    # Home
    path("", home, name="home"),

    # Authentication
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Dashboard
    path("dashboard/", dashboard, name="dashboard"),

    # Posts
    path("create-post/", create_post, name="create_post"),
    path("like/<int:post_id>/", like_post, name="like_post"),
    path("comment/<int:post_id>/", add_comment, name="add_comment"),

    # Profile
    path("profile/", profile, name="profile"),
    
    path("edit-profile/", edit_profile, name="edit_profile"),

    # Follow
    path("follow/<int:user_id>/", follow_user, name="follow_user"),

    # Explore
    path("explore/", explore, name="explore"),

    # Notifications
    path("notifications/", notifications, name="notifications"),

    path(
        "notifications/read/",
        mark_notifications_read,
        name="mark_notifications_read"
    ),

    path(
        "user/<int:user_id>/",
        user_profile,
        name="user_profile"
      ),
]