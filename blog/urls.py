from django.contrib.sitemaps.views import sitemap
from django.urls import path

from blog.feeds import LatestPostFeed
from blog.views import *
from blog.sitemaps import *

app_name = 'blog'

sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('', post_list, name='home'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('detail/<int:year>/<int:month>/<int:day>/<slug:post>', post_detail, name='post_detail'),
    path('share/<int:post_id>/', post_share, name='post_share'),
    path('comment/<int:post_id>/', post_comment, name='post_comment'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemaps'),
    path('feed/', LatestPostFeed(), name='post_feed'),
]