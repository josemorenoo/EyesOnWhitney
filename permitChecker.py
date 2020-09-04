#!/usr/bin/env python3

import json
import sys
from datetime import date, datetime, timedelta
from dateutil import rrule

import requests
from fake_useragent import UserAgent
import pprint

ISO_DATE_FORMAT_REQUEST = "%Y-%m-%dT00:00:00.000Z"
ISO_DATE_FORMAT_RESPONSE = "%Y-%m-%dT00:00:00Z"

SUCCESS_EMOJI = " 🏕 "
FAILURE_EMOJI = " ❌ "

headers = {"User-Agent": UserAgent().random}

def send_request(url, params, showResponse = False):
    resp = requests.get(url, params=params, headers=headers)
    if resp.status_code != 200:
        raise RuntimeError(
            "failedRequest",
            "ERROR, {} code received from {}: {}".format(
                resp.status_code, url, resp.text
            ),
        )
    if showResponse: 
        printResponse(resp)
    return resp.json()

def format_date(date_object, format_string=ISO_DATE_FORMAT_REQUEST):
    """
    This function doesn't manipulate the date itself at all, it just
    formats the date in the format that the API wants.
    """
    date_formatted = datetime.strftime(date_object, format_string)
    return date_formatted

def printResponse(resp):
    """
    pretty print wrapper for dictionary responses
    """
    print(pprint.PrettyPrinter(depth=8).pprint(resp))

def construct_endpoint(id, start_date, end_date):
    base_url          = "https://www.recreation.gov/api/permits/"
    availability_path = "{}/divisions/166/availability?".format(whitney_id)
    dates_path        = "start_date={}T00:00:00.000Z&end_date={}T00:00:00.000Z&commercial_acct=false".format(start_date, end_date)      
    return '{}{}{}'.format(base_url, availability_path, dates_path)

def construct_time_range(start_date, end_date):
    start_year, start_month, start_day = [int(x) for x in start_date.split('-')]
    end_year, end_month, end_day       = [int(x) for x in end_date.split('-')]
    start_of_month = datetime(start_year, start_month, start_day)
    end_date_dt    = datetime(end_year, end_month, end_day)
    return list(rrule.rrule(rrule.MONTHLY, dtstart=start_of_month, until=end_date_dt))[0]

def find_available_permits():
    successes = []

    dates = resp['payload']['date_availability']
    for date, availability in dates.items():
        remaining = availability['remaining']
        if (remaining > 0):
            day_available = date.split('T')[0]
            message = SUCCESS_EMOJI * 3 + ' Found {} permits on {}'.format(remaining, day_available)
            successes.append(message)
    return successes

if __name__ == "__main__":

    start_date = '2020-09-01'
    end_date   = '2020-10-15'
    whitney_id = 233260
    
    month_date = construct_time_range(start_date, end_date)
    params = {"start_date": format_date(month_date)}

    url = construct_endpoint(whitney_id, start_date, end_date)
    resp = send_request(url, params, showResponse=False)
    
    permits = find_available_permits()
    if len(permits) > 0:
        permits_available = '\n'.join(permits)
    else:
        permits_available = FAILURE_EMOJI + ' No permits found between {} and {}'.format(start_date, end_date)

    
    print(permits_available)
