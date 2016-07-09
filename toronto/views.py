from django.shortcuts import render
from datetime import date, timedelta
from toronto.models import TorontoBill, TorontoEvent, TorontoPerson, TorontoOrganization
from councilmatic_core.models import Action
from councilmatic_core.views import *
from django.conf import settings


class TorontoIndexView(IndexView):
    template_name = 'toronto/index.html'
    bill_model = TorontoBill
    event_model = TorontoEvent
    person_model = TorontoPerson

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        upcoming_meetings = list(self.event_model.upcoming_committee_meetings())

        date_cutoff = self.event_model.most_recent_past_city_council_meeting().start_time

        # populating activity at last council meeting
        meeting_activity = {}
        meeting_activity['actions'] = Action.actions_on_date(date_cutoff.date())
        meeting_bills = list(set([a.bill for a in meeting_activity['actions']]))
        meeting_activity['bills'] = meeting_bills
        meeting_activity['bills_routine'] = [b for b in meeting_bills if 'Routine' in b.topics]
        meeting_activity['bills_nonroutine'] = [b for b in meeting_bills if 'Non-Routine' in b.topics]




        # populating recent activitiy (since last council meeting)
        recent_activity = {}

        new_bills = TorontoBill.new_bills_since(date_cutoff)
        recent_activity['new'] = new_bills
        recent_activity['new_routine'] = [b for b in new_bills if 'Routine' in b.topics]
        recent_activity['new_nonroutine'] = [b for b in new_bills if 'Non-Routine' in b.topics]

        updated_bills = TorontoBill.updated_bills_since(date_cutoff)
        recent_activity['updated_routine'] = [b for b in updated_bills if 'Routine' in b.topics]
        recent_activity['updated_nonroutine'] = [b for b in updated_bills if 'Non-Routine' in b.topics]

        # getting topic counts for meeting bills
        topic_hierarchy = settings.TOPIC_HIERARCHY
        topic_tag_counts = {}
        for b in meeting_bills:
            for topic in b.topics:
                try:
                    topic_tag_counts[topic] += 1
                except KeyError:
                    topic_tag_counts[topic] = 1
        # put together data blob for topic hierarchy
        for parent_blob in topic_hierarchy:
            parent_blob['count'] = 0
            for child_blob in parent_blob['children']:
                child_name = child_blob['name']
                child_blob['count'] = topic_tag_counts[child_name] if child_name in topic_tag_counts else 0
                parent_blob['count'] += child_blob['count']
                for gchild_blob in child_blob['children']:
                    gchild_name = gchild_blob['name']
                    gchild_blob['count'] = topic_tag_counts[gchild_name] if gchild_name in topic_tag_counts else 0

        seo = {}
        seo.update(settings.SITE_META)
        seo.update({'site_url': settings.SITE_URL})
        seo['image'] = '/static/images/city_hall.jpg'

        return {
            'meeting_activity': meeting_activity,
            'recent_activity': recent_activity,
            'last_council_meeting': self.event_model.most_recent_past_city_council_meeting(),
            'next_council_meeting': self.event_model.next_city_council_meeting(),
            'upcoming_committee_meetings': upcoming_meetings,
            'topic_hierarchy': topic_hierarchy,
            'seo': seo,
        }

class TorontoAboutView(AboutView):
    template_name = 'toronto/about.html'


class TorontoBillDetailView(BillDetailView):
    model = TorontoBill

class TorontoCouncilMembersView(CouncilMembersView):

    def get_seo_blob(self):
        seo = {}
        seo.update(settings.SITE_META)
        seo['site_desc'] = "Look up your local Councillor, and see what they're doing in your ward & your city"
        seo['image'] = '/static/images/toronto_map.jpg'
        seo['title'] = 'Wards & Councillors - Toronto Councilmatic'

        return seo

class TorontoPersonDetailView(PersonDetailView):
    model = TorontoPerson

class TorontoEventsView(EventsView):
    def get_context_data(self, **kwargs):
        context = super(TorontoEventsView, self).get_context_data(**kwargs)
        return context

class TorontoEventDetailView(EventDetailView):
    template_name = 'toronto/event.html'

class TorontoCommitteeDetailView(CommitteeDetailView):
    model = TorontoOrganization
