from councilmatic_core.feeds import CouncilmaticFacetedSearchFeed
from toronto.models import TorontoBill
from haystack.query import SearchQuerySet

class TorontoCouncilmaticFacetedSearchFeed(CouncilmaticFacetedSearchFeed):
    # same as CouncilmaticFacetedSearchFeed but have a better item name template which uses
    # NYCBill's friendly_name() as opposed to Bill's friendly_name()
    #title_template = 'feeds/nyc_search_item_title.html'
    bill_model = TorontoBill
    # TODO: Is this required?
    sqs = SearchQuerySet().facet('bill_type')\
                          .facet('sponsorships')\
                          .facet('controlling_body')\
                          .facet('inferred_status')\
                          .facet('topics')\
                          .facet('wards')\
                          .facet('legislative_session')\
                          .highlight()

