from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
urlpatterns = [  
    # path('home',views.home,name='home' ),

    path('export',views.export,name='export' ),
    # path('create-dep/',views.createDep, name='create-dep' ),
    # path('update-dep/<str:pk>/',views.updateDep, name='update-dep' ),
    # path('delete-dep/<str:pk>/',views.deleteDep, name='delete-dep' ),

    path('create-tit/',views.createTit, name='create-tit' ),
    path('update-tit/<str:pk>/',views.updateTit, name='update-tit' ),
    path('delete-tit/<str:pk>/',views.deleteTit, name='delete-tit' ),

    path('create-form/',views.createForm, name='create-form' ),
    path('update-form/<str:pk>/',views.updateForm, name='update-form' ),
    path('delete-form/<str:pk>/',views.deleteForm, name='delete-form' ),

    path('login/',views.loginPage, name='login' ),
    path('register/',views.registerUser, name='register' ),
    path('logout/',views.logoutUser, name='logout' ),
 
    # path('profile/<str:pk>/',views.userProfile, name='profile' ),
    path('profile/<str:pk>/',views.userProfile, name='profile' ),
    path('update-user/',views.updateUser, name='update-user' ),

    path('tit-page/',views.titPage, name='tit-page' ),

    path('index/',views.index, name='index' ),

    path('charts',views.charts, name='charts' ),

    path('',views.userDashboard, name='home' ),
    path('user-dashm',views.userDashboard_m, name='user-dashm' ),

    path('manger-dash',views.mangerDashboard, name='manger-dash'),
    path('manger-dashm',views.mangerDashboard_m, name='manger-dashm'),

    path('dm-dash',views.dmdashboard, name='dm-dash' ),
    #password reset
    # submit email form
    path('reset_password/',
    auth_views.PasswordResetView.as_view(template_name="base/passreset.html"),
    name="reset_password"),
    #  email send succes message
    path('reset_password_sent/',
    auth_views.PasswordResetDoneView.as_view(template_name="base/passreset_sent.html"),
    name="password_reset_done"),
    # link to pass reset form in mail
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name="base/passreset_form.html"),
    name="password_reset_confirm"),
    # pass change complete
    path('password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name="base/passreset_complete.html"),
    name="password_reset_complete"),
]
