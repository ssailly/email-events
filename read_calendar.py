from arrow import now
from ics import Calendar
import sys
from urllib import request
import yaml

CALENDARS_FILE = 'calendars.yaml'
with open(CALENDARS_FILE, 'r') as f:
  calendars = yaml.safe_load(f)

def url_to_page(url):
  return request.urlopen(url).read().decode('utf8')

def page_to_calendar(page):
  try:
    return Calendar(page)
  except Exception as e:
    print(e)

def event_to_str(e):
    return '* ' + e.begin.format('YYYY-MM-DD') + ' ' + e.begin.format('HH:mm') + ' — ' + e.end.format('HH:mm') + ': ' + e.name

def get_next_events_str():
  next_events = ''
  for cal_name in calendars:
    c = calendars[cal_name]
    next_events += c['name'] + '\n'
    page = url_to_page(c['url'])
    cal = page_to_calendar(page)
    events_two_weeks = cal.timeline.included(now(), now().shift(weeks = 2))
    old_next_events = next_events
    for e in events_two_weeks:
      next_events += event_to_str(e) + '\n'
    if next_events == old_next_events:
      next_events += 'No events in this calendar\n'
    next_events += '\n'
  return next_events[:-2]
