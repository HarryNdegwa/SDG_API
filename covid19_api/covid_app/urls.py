from django.urls import path

from . import views

urlpatterns = [
    path("api/v1/on-covid-19/",views.PostCovidDataView.as_view(),name="post_covid_data"),
    path("api/v1/on-covid-19/json/",views.PostCovidDataView.as_view(),name="post_covid_data"),
    path("api/v1/on-covid-19/xml/",views.PostCovidXMLDataView.as_view(),name="post_covid_data"),
    path("api/v1/on-covid-19/logs/",views.GetLogsView.as_view(),name="logs")
]