from django.urls import path
from .views import ScrapeView, ScrapeResultView

urlpatterns = [
    path('scrape/', ScrapeView.as_view(), name='scrape'),
    path('scrape/<str:scrape_id>/', ScrapeResultView.as_view(), name='scrape_result'),
]
