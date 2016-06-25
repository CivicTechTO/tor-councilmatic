from councilmatic_core.haystack_indexes import BillIndex
from haystack import indexes
from chicago.models import ChicagoBill
from councilmatic_core.models import Post
from datetime import datetime
from django.conf import settings
from django.forms import model_to_dict
import pytz

app_timezone = pytz.timezone(settings.TIME_ZONE)
ocd_division_id = settings.OCD_JURISDICTION_ID.replace('ocd-jurisdiction', 'ocd-division').replace('/legislature', '')

class ChicagoBillIndex(BillIndex, indexes.Indexable):

    topics = indexes.MultiValueField(faceted=True)
    wards = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return ChicagoBill

    def prepare(self, obj):
        data = super(ChicagoBillIndex, self).prepare(obj)

        boost = 0
        if obj.last_action_date:
            now = app_timezone.localize(datetime.now())

            # obj.last_action_date can be in the future
            weeks_passed = (now - obj.last_action_date).days / 7 + 1
            boost = 1 + 1.0 / max(weeks_passed, 1)

        data['boost'] = boost

        return data

    def prepare_topics(self, obj):
        return obj.topics

    def prepare_wards(self, obj):
        return [Post.objects.all().get(division_ocd_id=ocd_division_id+'/ward:'+ward).label for ward in obj.wards]

    # TODO: Revert this workaround
    def prepare_actions(self, obj):
        return [action.description for action in obj.actions.all()]

    def prepare_sponsorships(self, obj):
        return [sponsorship.person.name for sponsorship in obj.sponsorships.all()]

