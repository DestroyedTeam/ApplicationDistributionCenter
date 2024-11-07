from django.urls import path
from . import views


urlpatterns = [
        # 页面路由
        path('', views.question_list_page, name='question_page'),
        path('detail', views.question_detail_page, name='question_detail_page'),

        # API路由
        path("api/questions", views.get_questions, name='get_questions'),
        path("api/adopt", views.adopt_answer, name='adopt_answer'),
        path("api/ask", views.ask_question, name='ask_question'),
        path("api/answer", views.answer_question, name='answer_question'),
    ]