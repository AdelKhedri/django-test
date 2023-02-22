from django.urls import path
from .views import (home, diteils, login_n, sinup, logout_t, delete_account, report, PostListView, PostCreateView, PostUpdateView,
                    PostDeleteView, home_, test, not_found, PostDetailView,orm,cofirm)
urlpatterns = [
    path('', home),
    path('<int:id>', diteils),
    path('not/', not_found),
    path('login/', login_n),
    path('sinup/', sinup),
    path('active_phone/', cofirm, name='active_phone'),
    path('logout/', logout_t),
    path('delete_account/', delete_account),
    path('reportuser/', report),
    path('pl/', PostListView.as_view(), name='postlist'),
    path('pc/', PostCreateView.as_view()),
    path('pu/<pk>/', PostUpdateView.as_view(), name='postupdate'),
    path('pdel/<pk>/', PostDeleteView.as_view(), name='postdelete'),
    path('pd/<pk>/', PostDetailView.as_view(), name='postdetail'),
    path('orm',orm, name='orm',)
]