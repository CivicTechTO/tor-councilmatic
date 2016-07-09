"""councilmatic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from haystack.query import SearchQuerySet
from councilmatic_core.views import CouncilmaticSearchForm, CouncilmaticFacetedSearchView
from councilmatic_core.feeds import CouncilmaticFacetedSearchFeed, BillDetailActionFeed
from chicago.views import *
from chicago.feeds import *

sqs = SearchQuerySet().facet('bill_type')\
                      .facet('sponsorships')\
                      .facet('controlling_body')\
                      .facet('inferred_status')\
                      .facet('topics')\
                      .facet('legislative_session')\
                      .facet('wards')\
                      .highlight()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/rss/', TorontoCouncilmaticFacetedSearchFeed(), name='councilmatic_search_feed'),
    url(r'^search/', CouncilmaticFacetedSearchView(searchqueryset=sqs,
                                       form_class=CouncilmaticSearchForm), name='councilmatic_search'),
    url(r'^$', TorontoIndexView.as_view(), name='index'),
    url(r'^about/$', TorontoAboutView.as_view(), name='about'),
    url(r'^legislation/(?P<slug>[^/]+)/$', TorontoBillDetailView.as_view(), name='bill_detail'),
    url(r'^legislation/(?P<slug>[^/]+)/rss/$', BillDetailActionFeed(), name='bill_detail_action_feed'),
    url(r'^person/(?P<slug>[^/]+)/$', TorontoPersonDetailView.as_view(), name='person'),
    url(r'^council-members/$', TorontoCouncilMembersView.as_view(), name='council_members'),
    url(r'^events/', TorontoEventsView.as_view(), name='events'),
    url(r'^event/(?P<slug>.*)/$',
        TorontoEventDetailView.as_view(), name='event_detail'),
    url(r'', include('councilmatic_core.urls')),
    url(r'^members/$', RedirectView.as_view(url='/council-members/', permanent=True), name='council_members'),
]
