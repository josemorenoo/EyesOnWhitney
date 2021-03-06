#!/usr/bin/env python3

import json
import sys
from datetime import date, datetime, timedelta
from dateutil import rrule
import requests
from fake_useragent import UserAgent
import pprint

from whitneymail import create_email_message
from whitneymail import send_word_at_once

import schedule
import time


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

def construct_endpoint(permit_id, start_date, end_date):
    base_url          = "https://www.recreation.gov/api/permits/"
    availability_path = "{}/divisions/166/availability?".format(permit_id)
    dates_path        = "start_date={}T00:00:00.000Z&end_date={}T00:00:00.000Z&commercial_acct=false".format(start_date, end_date)      
    return '{}{}{}'.format(base_url, availability_path, dates_path)

def construct_time_range(start_date, end_date):
    start_year, start_month, start_day = [int(x) for x in start_date.split('-')]
    end_year, end_month, end_day       = [int(x) for x in end_date.split('-')]
    start_of_month = datetime(start_year, start_month, start_day)
    end_date_dt    = datetime(end_year, end_month, end_day)
    return list(rrule.rrule(rrule.MONTHLY, dtstart=start_of_month, until=end_date_dt))[0]

def get_weekday(daystring):
    # daystring format - 2020-01-01
    y, m, d = daystring.split('-')
    date_int = date(int(y), int(m), int(d)).weekday()
    if (date_int == 0): return 'Monday'
    if (date_int == 1): return 'Tuesday'
    if (date_int == 2): return 'Wednesday'
    if (date_int == 3): return 'Thursday'
    if (date_int == 4): return 'Friday'
    if (date_int == 5): return 'Saturday'
    elif (date_int == 6): return 'Sunday'

def find_available_permits(resp):
    successes = []

    dates = resp['payload']['date_availability']
    for date, availability in dates.items():
        remaining = availability['remaining']
        if (remaining > 0):
            day_available = date.split('T')[0]
            message = SUCCESS_EMOJI + ' Found {} permits on {} [{}]'.format(str(remaining), day_available, get_weekday(day_available))
            successes.append(message)
    return successes

if __name__ == "__main__":

    def job():
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        people_who_care = ['josemoreno181818@gmail.com', 'jose.moreno@capitalone.com', 'nfarias@berkeley.edu', 'mcdermenator@gmail.com']
        start_date = '2020-09-01'
        end_date   = '2020-10-15'
        whitney_id = 233260
        
        month_date = construct_time_range(start_date, end_date)
        params = {"start_date": format_date(month_date)}

        url = construct_endpoint(whitney_id, start_date, end_date)
        resp = send_request(url, params, showResponse=False)
        
        
        # this mocks the finding of a permit
        '''
        permits = [
            SUCCESS_EMOJI + ' Found {} permits on {} [{}]'.format(str(1), "2020-08-01", get_weekday("2020-08-01")),
            SUCCESS_EMOJI + ' Found {} permits on {} [{}]'.format(str(4), "2020-09-01", get_weekday("2020-09-01")),
            SUCCESS_EMOJI + ' Found {} permits on {} [{}]'.format(str(2), "2020-10-01", get_weekday("2020-10-01"))
        ]
        '''
        
        permits = find_available_permits(resp)
        seen_permits = set()
        if len(permits) > 0:
            permits_available = ''
            for permit in permits:
                if permit not in seen_permits:
                    seen_permits.add(permit)
                    permits_available += '\n' + permit 
            if permits_available is not '':
                send_word_at_once(people_who_care, permits_available)
            print(permits_available)
        else:
            permits_available = FAILURE_EMOJI + ' No permits found between {} [{}] and {} [{}]'.format(start_date, get_weekday(start_date), end_date, get_weekday(end_date))
            print(permits_available)

    # runs continuously in the terminal, check every five min if SCHEDULE
    SCHEDULE = True 
    
    if (SCHEDULE):
        schedule.every(5).minutes.do(job)
        while True:
            schedule.run_pending()
            time.sleep(1)
    else: # run once
        job()
    
