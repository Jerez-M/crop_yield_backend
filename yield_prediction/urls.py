from . import views
from django.urls import path


urlpatterns = [
    path("predict/", views.YieldPredictionView.as_view(), name="YieldPredictionView"),
    path('<int:pk>/', views.RetrieveCropData.as_view(), name="RetrieveCropData"),
    path('get-all/', views.RetrieveAllCropData.as_view()),
    path('get-crop-data-by-year/<int:year>', views.RetrieveCropDataByYearView.as_view()),
    path('', views.createCropData.as_view()),
]
