from django.test import TestCase
from django.http import HttpRequest
from django.test import SimpleTestCase
from django.urls import reverse
from map.models import Routes,Stops,CalendarService,CalendarExceptions,Shapes,Trips,MapTripStopTimes
from map.views import change_to_timestamp, predict, get_current_weather, get_weather_forecast, get_time_period, MultiRoutes, Trip, DirectRoutes
import datetime
from datetime import timedelta

class IndexPageTests(TestCase):
    def test_index_page_status_code(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_index_url_by_name(self):
        response = self.client.get(reverse('home_page'))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home_page'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/index.html')

    def test_inedx_page_contains_correct_html(self):
        response = self.client.get('/')
        self.assertContains(response, '<div id="map"></div>')

    def test_index_page_does_not_contain_incorrect_html(self):
        response = self.client.get('/')
        self.assertNotContains(response, "This should not be contained")


class RoutingTests(TestCase):

    def test_change_to_timestamp(self):
        time = datetime.time(14,30,00)
        seconds = (((time.hour * 60) + time.minute) * 60) + time.second

        now = datetime.datetime.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        predicted_timestamp = (now.timestamp() + seconds) * 1000

        self.assertEquals(change_to_timestamp(time), predicted_timestamp)

    def test_predict(self):
        stop_sequence_list = []
        for i in range(30):
            stop_sequence_list.append(i+1)

        x = predict(15, 0.2, 65, 2, 1, "46A", stop_sequence_list)
        self.assertEquals(len(x), 30)
        self.assertEquals(x[2], -0.5930987289207879)
        self.assertEquals(x[26], 1.3388085810639405)

    def test_get_current_weather(self):

        x = get_current_weather()
        self.assertEquals(len(x), 3)
        self.assertTrue(-20 <= x[0] <= 50)
        self.assertTrue(0 <= x[2] <= 100)

    def test_get_weather_forecast(self):

        today = datetime.datetime.now()
        tomorrow = today + timedelta(days=1)

        x = get_weather_forecast(today)

        self.assertEquals(len(x), 3)
        self.assertTrue(-20 <= x[0] <= 50)
        self.assertTrue(0 <= x[2] <= 100)

        x = get_weather_forecast(tomorrow)

        self.assertEquals(len(x), 3)
        self.assertTrue(-20 <= x[0] <= 50)
        self.assertTrue(0 <= x[2] <= 100)

    def test_get_weather_forecast_backup(self):

        invalid_date = datetime.datetime.strptime('Jun 1 2022  1:33PM', '%b %d %Y %I:%M%p')

        x = get_weather_forecast(invalid_date)

        self.assertEquals(len(x), 3)
        self.assertEquals(x[0], 15)
        self.assertEquals(x[1], 0)
        self.assertEquals(x[2], 80)

    def test_get_time_period(self):

        time1 = datetime.time(3,30,00)
        time2 = datetime.time(7,30,00)
        time3 = datetime.time(16,30,00)

        x1 = get_time_period(time1)
        x2 = get_time_period(time2)
        x3 = get_time_period(time3)

        self.assertEquals(x1,0)
        self.assertEquals(x2,5)
        self.assertEquals(x3,4)
