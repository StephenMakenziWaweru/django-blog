from django.urls import path
from .views import (about, PostListView, PostCreateView,
                    PostUpdateView, PostDetailView, PostDeleteView,
                    download)

urlpatterns = [
    path('', PostListView.as_view(), name = 'home'),
    path('newpost/', PostCreateView.as_view(), name = 'newpost'),
    path('download/', download, name = 'download'),
    path('<int:pk>/updatepost/', PostUpdateView.as_view(), name = 'updatepost'),
    path('<int:pk>/detailedpost/', PostDetailView.as_view(), name = 'detailedpost'),
    path('<int:pk>/deletepost/', PostDeleteView.as_view(), name = 'deletepost'),
    path('about/', about, name='about'),
]
