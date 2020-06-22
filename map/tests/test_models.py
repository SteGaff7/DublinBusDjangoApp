from django.test import TestCase
from django.urls import reverse
from map.models import Routes,Stops,CalendarService,CalendarExceptions,Shapes,Trips,MapTripStopTimes
import json

class TestModels(TestCase):

    def setUp(self):

        self.route1=Routes.objects.create(route_id = "46A", agency_id = "Jackson",
                                          route_short_name = "46")

        self.stop1=Stops.objects.create(stop_id = "848", stop_id_short = 848,
                                        stop_name = "Donnybrook", stop_lat = 6.35, stop_lng =54.34)

        self.calendarService1=CalendarService.objects.create(service_id = "20180101", start_date ='2019-06-16',
                                                            end_date = '2019-08-24', monday = True, tuesday = False,
                                                            wednesday =False, thursday = False,
                                                            friday = False, saturday = False, sunday = False)

        self.calendarException1= CalendarExceptions.objects.create(service_id = self.calendarService1,
                                                                    exception_date = '2019-08-24', exception_type = 1)

        self.shape1= Shapes.objects.create(shape_id = "circle",
                                            shape_point_lat = 6.38, shape_point_lng = 54.29,
                                            shape_point_sequence = 7, shape_dist_travelled = 9.76)

        self.trips1= Trips.objects.create(trip_id = "39A", route_id = self.route1, direction = True, trip_headsign = "Headsign", shape_id = "5", service_id = self.calendarService1)


    def test_Routes_is_created_correctly(self):

        self.assertEquals(self.route1.route_id,"46A")


    def test_Stops_is_created_correctly(self):

        self.assertEquals(self.stop1.stop_name, "Donnybrook")
        self.assertEquals(self.stop1.stop_lat,6.35)


    def test_CalendarService_is_created_correctly(self):

        self.assertEquals(self.calendarService1.service_id, "20180101")
        self.assertEquals(self.calendarService1.thursday, False)


    def test_CalendarExceptions_is_created_correctly(self):

        self.assertEquals(self.calendarException1.service_id, self.calendarService1)
        self.assertEquals(self.calendarException1.exception_type, 1)


    def test_Shapes_is_created_correctly(self):

        self.assertEquals(self.shape1.shape_id , "circle")


    def test_Trips_is_created_correctly(self):

        self.assertEquals(self.trips1.route_id, self.route1)
        self.assertEquals(self.trips1.trip_id,"39A")
