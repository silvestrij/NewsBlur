import datetime
from django.shortcuts import get_object_or_404
from apps.rss_feeds.models import Feed, StoriesPerMonth
from utils import json

@json.json_view
def load_feed_statistics(request):
    stats = dict()
    feed_id = request.GET['feed_id']
    feed = get_object_or_404(Feed, pk=feed_id)
    
    # Dates of last and next update
    stats['last_update'] = feed.last_update
    stats['next_update'] = feed.next_scheduled_update
    
    # Minutes between updates
    now = datetime.datetime.now()
    next_scheduled_update, random_factor = feed.get_next_scheduled_update()
    delta = now - next_scheduled_update - datetime.timedelta(minutes=random_factor)
    stats['update_interval_minutes'] = delta.seconds / 60
    
    # Stories per month - average and month-by-month breakout
    stories_last_year, average_per_month = StoriesPerMonth.past_year(feed)
    stats['stories_last_year'] = stories_last_year and json.decode(stories_last_year)
    stats['average_per_month'] = average_per_month
    
    # Subscribers
    stats['subscriber_count'] = feed.num_subscribers
    
    return stats