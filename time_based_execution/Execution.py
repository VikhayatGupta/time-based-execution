import logging
import time
from datetime import datetime

import pandas as pd
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder

logging.basicConfig(level=logging.INFO, filename='timebasedexec.log')


class TimeBasedExectuion:
    def __init__(self, file_path="config.csv"):
        self.file_path = file_path

    def read_configs(self):
        data = pd.read_csv(self.file_path).fillna('all')
        return data.values

    @staticmethod
    def check_timezone(country: str):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(country, timeout=10)
            obj = TimezoneFinder()
            return obj.timezone_at(lng=location.longitude, lat=location.latitude)
        except Exception:
            logging.exception("Exception Railed while getting timezone based on country")

    def check_time_day(self, country: str):
        try:
            timezone = self.check_timezone(country)
            tz = pytz.timezone(timezone)
            ct = datetime.now(tz=tz)
            return ct.strftime('%A'), ct.strftime('%H:%M:%S')
        except Exception:
            logging.exception("Exception Railed while fetching time and day")

    @staticmethod
    def is_time_between(begin_time: str, end_time: str, check_time: str):

        logging.info(f"Start time: {begin_time} End time: {end_time} current time: {check_time}")
        if begin_time < end_time:
            return check_time >= begin_time and check_time <= end_time
        else:
            return check_time >= begin_time or check_time <= end_time

    def execution(self):
        try:
            for data in self.read_configs():
                logging.info(f"executing :{data}")
                country_timezone = self.check_timezone(data[2])
                check_time_day = self.check_time_day(country_timezone)
                if "all" in data:
                    if self.is_time_between(data[3], data[4], check_time_day[1]):
                        logging.info("True")
                    else:
                        logging.info("False")
                else:
                    days = str(data[-1]).split(" and ")
                    if check_time_day[0] not in days:
                        logging.info("False")
                    elif self.is_time_between(data[3], data[4], check_time_day[1]):
                        logging.info("True")
                    else:
                        logging.info("False")
        except Exception:
            logging.exception("Exception Railed while doing Execution")

    def monitor_and_execute(self):
        while True:
            self.execution()
            time.sleep(60)
