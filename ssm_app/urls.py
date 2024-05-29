from django.urls import path

from ssm_app.views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', homepage, name='home'),
    path('music/', show_music_view, name='music'),
    path('blog/', show_blog_view, name='blog'),
    # SUBSCRIPTION
    path('subscription/', subscribe_view, name='subscribe'),
    # REGISTRATION
    path('register/', register_view, name='register'),
    # LOGIN
    path('login/', login_view, name='login'),
    # LOGOUT
    path('logout/', logout_view, name='logout'),
    # PASSWORD CHANGE
    path('password/', PasswordsChangeView.as_view(), name='change_password'),
    # PASSWORD CHANGE_SUCCESSFUL
    path('password_success/', password_success, name='password_success'),

    # PASSWORD RESET
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='forgot_password/password_reset.html'),
         name='reset_password'),
    # PASSWORD RESET DONE
    path('reset-password-sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='forgot_password/password_reset_done.html'),
         name='password_reset_done'),
    # PASSWORD RESET CONFIRM (Link in email)
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='forgot_password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    # PASSWORD RESET COMPLETE (Success message)
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='forgot_password/password_reset_complete.html'),
         name='password_reset_complete'),

    # Checkout session Stripe:
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),

    # CREATE LIBRARY
    path('create-playlist/', PlaylistCreateView.as_view(), name='playlist_create'),
    # LIBRARY
    path('playlist-list/', PlaylistListView.as_view(), name='playlist'),
    path('add-song-to-playlist/', add_song_to_playlist_view, name='add_song_to_playlist'),
    path('success/', success_view, name='success'),
    path('cancel/', cancel_view, name='cancel'),
    path('music/', show_music_view, name='music'),
    path('blog/', show_blog_view, name='blog'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('subscription/', subscribe_view, name='subscribe'),
    # path('register/', register_view, name='register'),
    # path('login/', login_view, name='login'),
    # path('logout/', logout_view, name='logout'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    # path('subscription/', show_subscription_view, name="subscription"),
    path('your_playlist/<int:pk>/', your_playlist, name='your_playlist'),
    path('delete/<int:id>/', delete_song_from_playlist, name='delete'),
]
