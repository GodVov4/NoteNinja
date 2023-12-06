from django.urls import path

from . import views

app_name = 'noteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('note/', views.note, name='note'),
    path('note/detail/<int:note_id>', views.detail, name='detail'),
    path('note/done/<int:note_id>', views.set_done, name='set_done'),
    path('note/edit_note/<int:note_id>', views.edit_note, name='edit_note'),
    path('note/delete_note/<int:note_id>', views.delete_note, name='delete_note'),
    path('tag/edit_tag/<int:tag_id>', views.edit_tag, name='edit_tag'),
    path('tag/delete_tag/<int:tag_id>', views.delete_tag, name='delete_tag'),
]
