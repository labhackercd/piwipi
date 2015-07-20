# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import sys
import json
import datetime
from functools import partial

import click
import pytz
import dateutil.parser
from pyexchange import Exchange2010Service, ExchangeNTLMAuthConnection


DEFAULT_TIMEZONE = 'America/Sao_Paulo'


click_required_option = partial(click.option, required=True)


class EventEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        elif isinstance(o, set):
            return tuple(o)
        elif isinstance(o, Exchange2010Service):
            return repr(o)
        else:
            return super(EventEncoder, self).default(o)


def should_keep_item(k):
    return k != 'service'


def as_event_dict(event):
    # XXX Just aliasing here, please don't change it directly or bad things can happen!
    event_dict = event.__dict__

    # Return a copy of the event's dict without some items.
    return dict((k, event_dict[k]) for k in event_dict.keys() if should_keep_item(k))


def get_all_calendar_events(service, username, password, start, end, details):
    connection = ExchangeNTLMAuthConnection(service, username, password, verify_certificate=False)

    service = Exchange2010Service(connection)

    events = service.calendar().list_events(start=start, end=end, details=details)

    return map(as_event_dict, events.events)


@click.command()
@click_required_option('--service', help='Exchange service URL. Like https://ce.camara.leg.br/EWS/Exchange.asmx.')
@click_required_option('--username', help='Exchange user name.')
@click_required_option('--password',  help='Exchange user password.')
@click_required_option('--start', help='Start date. Format YYYY-MM-DD.')
@click_required_option('--end', help='End date. Format YYYY-MM-DD.')
@click_required_option('--timezone', '-Z', default=DEFAULT_TIMEZONE,
                       help='Dates time zone. Defaults to {0}.'.format(DEFAULT_TIMEZONE))
@click.option('--details/--no-details', default=False)
def main(service, username, password, start, end, timezone, details):

    start = dateutil.parser.parse(start)
    end = dateutil.parser.parse(end)

    timezone = pytz.timezone(timezone)
    start = timezone.localize(start)
    end = timezone.localize(end)

    events = get_all_calendar_events(service, username, password, start, end, details)

    print(json.dumps(events, cls=EventEncoder, indent=2, skipkeys=True))

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
