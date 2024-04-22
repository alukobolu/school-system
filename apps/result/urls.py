from django.urls import path

from .views import ResultListView, create_result, edit_results, edit_student_results,view_result,add_comment

urlpatterns = [
    path("create/", create_result, name="create-result"),
    path("edit-results/", edit_results, name="edit-results"),
    path("edit-student-results/", edit_student_results, name="edit-student-results"),
    path("edit-results/", edit_results, name="edit-results"),
    path("view-result/", view_result, name="view-single-result"),
    path("add-comment/", add_comment, name="add-comment"),
    # path("view/all", ResultListView.as_view(), name="view-results"),
    path("view/class/<class_id>", ResultListView.as_view(), name="view-a-result"),
]
