from django.urls import path
from . import views

urlpatterns = [
    path('', views.library, name="library"),
    path('lib_create/', views.lib_create, name="lib_create"),
    path('<int:lib_id>/rename/', views.rename_library, name="rename_library"),
    path('<int:book_id>/<int:lib_id>/update/', views.update, name="update"),
    path('<int:book_id>/<int:lib_id>/update_issued_book/', views.update_issued_book, name="update_issued_book"),
    path('<int:lib_id>/lib_del/', views.lib_del, name="lib_del"),
    path('<int:lib_id>/add_book/', views.add_book, name="add_book"),
    path('<int:book_id>/<int:lib_id>/issue_book/', views.issue_book, name="issue_book"),
    path('<int:lib_id>/issued_books/', views.issued_books, name="issued_books"),
    path('<int:book_id>/<int:lib_id>/return_book/', views.return_book, name="return_book"),
    path('<int:lib_id>/open/', views.open, name="open"),
    path('<int:book_id>/<int:lib_id>/remove/', views.remove, name='remove'),
    path('register/', views.register, name="register"),
    path('logout/', views.logged_out, name='logged_out'),
]
