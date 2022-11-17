import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy

from blog.models import Post


class LatestPostFeed(Feed):
    title_template = 'Blognificent'
    title = 'Blognificent'
    link = reverse_lazy('blog:post_list')
    description_template = 'New posts from Blognificent'
    description = 'New posts from Blognificent'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.content), 30)

    def item_pubdate(self, item):
        return item.publish

