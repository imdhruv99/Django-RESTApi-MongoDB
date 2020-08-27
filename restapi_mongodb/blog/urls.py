from django.conf.urls import url

from blog import views


urlpatterns = [

    url(r'^api/blogs$', views.blog_list),
    
    url(r'^api/blogs/(?P<pk>[0-9]+)$', views.blog_detail),
    
    url(r'^api/blogs/published$', views.blog_list_published)

]