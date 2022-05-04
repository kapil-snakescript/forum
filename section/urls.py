from django.urls import  path
from .views import home,add_section,edit_section,delete_section,post_list


urlpatterns = [

      path('',home,name='section-list'),
      path('add-section/',add_section,name='add-section'),
      path('edit-section/<int:pk>/',edit_section,name='edit-section'),
      path('delete-section/<int:pk>/',delete_section,name='delete-section'),
      path("postlist/<int:section_id>", post_list, name="post_list"),
]