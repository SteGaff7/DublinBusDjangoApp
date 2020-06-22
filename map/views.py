
from django.shortcuts import render, redirect
from django.http import JsonResponse

import json
import requests
import datetime
import pandas as pd
import psycopg2

from sklearn.externals import joblib
from datetime import date
from .models import MapTripStopTimes, Stops, CalendarService, Trips, Routes, Shapes


def home_page(request):
    ''' Simple view that renders the index html template with all the bus stop information
        using Jinja2
    '''
    bus_stops = Stops.objects.all()
    bus_stop_list = []
    for bus_stop in bus_stops:
        bus_stop_list.append((bus_stop.stop_id, bus_stop.stop_id_short, bus_stop.stop_name, bus_stop.stop_lat, bus_stop.stop_lng))

    return render(request, 'map/index.html', {'JSONdata': json.dumps(bus_stop_list)})



def return_routes(request):
    '''
    Function that returns the routes if any between 2 specified bus stops using an optional
    specified time and date
    '''

    start_stop = request.GET['startstop']
    dest_stop = request.GET['endstop']

    start_stop = Stops.objects.get(stop_id_short = start_stop)
    dest_stop = Stops.objects.get(stop_id_short = dest_stop)

    time_specified = request.GET['time_specified']
    date_specified = request.GET['date_specified']

    # Now option and an empty later option
    if time_specified == '' and date_specified == '':
        time_specified = (datetime.datetime.now()).strftime('%H:%M:%S')
        specified_date_time = datetime.datetime.now()

        weather = get_current_weather()
        weather_temp = weather[0]
        weather_rain = weather[1]
        weather_humidity = weather[2]

    # Date not specfied
    elif date_specified == '':
        time_specified = time_specified + ":00"
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        specified_date_time = datetime.datetime.strptime(today_date + "-" + time_specified, '%Y-%m-%d-%H:%M:%S')

        weather = get_weather_forecast(specified_date_time)
        weather_temp = weather[0]
        weather_rain = weather[1]
        weather_humidity = weather[2]

    # Time not specfied
    elif time_specified == '':
        time_specified = (datetime.datetime.now()).strftime('%H:%M:%S')
        specified_date_time = datetime.datetime.strptime(date_specified + "-" + time_specified, '%m/%d/%y-%H:%M:%S')

        weather = get_weather_forecast(specified_date_time)
        weather_temp = weather[0]
        weather_rain = weather[1]
        weather_humidity = weather[2]

    # Both specfied
    else:
        time_specified = time_specified + ":00"
        specified_date_time = datetime.datetime.strptime(date_specified + "-" + time_specified, '%m/%d/%y-%H:%M:%S')

        weather = get_weather_forecast(specified_date_time)
        weather_temp = weather[0]
        weather_rain = weather[1]
        weather_humidity = weather[2]

    # Convert time to time period
    time_period = get_time_period(specified_date_time)

    # Monday is 0
    day = specified_date_time.weekday()

    # Set time ranges for range of trips to return
    start_range = (specified_date_time + datetime.timedelta(minutes=-5)).strftime('%H:%M:%S')
    end_range = (specified_date_time + datetime.timedelta(minutes=20)).strftime('%H:%M:%S')
    start_changeover = (specified_date_time).strftime('%H:%M:%S')
    changeover_range = (specified_date_time + datetime.timedelta(minutes=100)).strftime('%H:%M:%S')

    #Get service IDs for specified date
    if day == 0:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = specified_date_time, end_date__gte = specified_date_time, monday = True))
        weekday = True
    elif day == 1:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = specified_date_time, end_date__gte = specified_date_time, tuesday = True))
        weekday = True
    elif day == 2:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = specified_date_time, end_date__gte = specified_date_time, wednesday = True))
        weekday = True
    elif day == 3:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = specified_date_time, end_date__gte = specified_date_time, thursday = True))
        weekday = True
    elif day == 4:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = specified_date_time, end_date__gte = specified_date_time, friday = True))
        weekday = True
    elif day == 5:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = specified_date_time, end_date__gte = specified_date_time, saturday = True))
        weekday = False
    elif day == 6:
        service_list = list(CalendarService.objects.values_list('service_id', flat = True).filter(start_date__lte = specified_date_time, end_date__gte = specified_date_time, sunday = True))
        weekday = False

    # Get all trips of starting bus stop that are within a time range specified by user
    trip_id_list = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(stop_id = start_stop, arrival_time__range = (start_range, end_range)))

    # Narrow the trips to those that have service on todays date
    valid_trip_id_list = list(Trips.objects.values_list('trip_id', flat = True).filter(trip_id__in = trip_id_list, service_id__in = service_list))

    # Get trips that are also specfic to destination stop
    common_trip_id_list = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(trip_id__in = valid_trip_id_list, stop_id = dest_stop))

    # Create dictionary of routes possible between stops
    data = []

    # If no common trips between the two stops
    if len(common_trip_id_list) == 0:

        valid_start_stop_trip_ids = valid_trip_id_list

        # Dest stop trip ids within a larger time frame
        dest_stop_trip_ids = list(MapTripStopTimes.objects.values_list('trip_id', flat = True).filter(stop_id = dest_stop, arrival_time__range = (start_changeover, changeover_range)))

        valid_dest_stop_trip_ids = list(Trips.objects.values_list('trip_id', flat = True).filter(trip_id__in = dest_stop_trip_ids, service_id__in = service_list))

        travel_options = MultiRoutes(weather_temp, weather_rain, weather_humidity, weekday, time_specified, time_period, start_stop, dest_stop, valid_start_stop_trip_ids, valid_dest_stop_trip_ids)

        # If valid travel options using multi-route
        if len(travel_options.multi_trips_list) != 0:
            for travel_option in travel_options.multi_trips_list:

                route_option_dict = {}

                route_option_dict["direct"] = False
                route_option_dict["start_stop_id"] = travel_option["stage1"].start_stop_id
                route_option_dict["dest_stop_id"] = travel_option["stage2"].dest_stop_id
                route_option_dict["start_stop_id_short"] = travel_option["stage1"].start_stop_id_short
                route_option_dict["dest_stop_id_short"] = travel_option["stage2"].dest_stop_id_short

                route_option_dict["stages"] = travel_option["stages"]
                route_option_dict["changeover_stop_id"] = travel_option["changeover_stop_id"]
                route_option_dict["changeover_stop_id_short"] = travel_option["changeover_stop_id_short"]
                route_option_dict["start_stop_predicted_arrival_time"] = travel_option["start_stop_predicted_arrival_time"]
                route_option_dict["start_stop_predicted_arrival_timestamp"] = change_to_timestamp(route_option_dict["start_stop_predicted_arrival_time"])
                route_option_dict["changeover_stop_predicted_arrival_time"] = travel_option["changeover_stop_predicted_arrival_time"]
                route_option_dict["changeover_stop_predicted_arrival_timestamp"] = change_to_timestamp(route_option_dict["changeover_stop_predicted_arrival_time"])
                route_option_dict["stage1_time"] = travel_option["stage1_time"]
                route_option_dict["wait_time"] = travel_option["wait_time"]
                route_option_dict["stage2_time"] = travel_option["stage2_time"]
                route_option_dict["total_time"] = travel_option["total_time"]


                stage_dict = {}

                stage_dict["route_id"] = travel_option["stage1"].route_id
                stage_dict["trip_id"] = travel_option["stage1"].trip_id
                stage_dict["route_short_name"] = travel_option["stage1"].route_short_name
                stage_dict["trip_headsign"] = travel_option["stage1"].trip_headsign
                stage_dict["start_stop_id"] = travel_option["stage1"].start_stop_id
                stage_dict["dest_stop_id"] = travel_option["changeover_stop_id"]
                stage_dict["start_stop_id_short"] = travel_option["stage1"].start_stop_id_short
                stage_dict["dest_stop_id_short"] = travel_option["changeover_stop_id_short"]
                stage_dict["number_stops"] = len(travel_option["stage1_subroute_stops"])
                stage_dict["departure_time"] = travel_option["stage1"].departure_time
                stage_dict["all_stops_list"] = travel_option["stage1"].all_stops_list
                stage_dict["stage_subroute_stops"] = travel_option["stage1_subroute_stops"]
                stage_dict["route_shape_points"] = travel_option["stage1"].route_shape_points
                stage_dict["stage1_subroute_shape_points"] = travel_option["stage1_subroute_shape_points"]


                route_option_dict["stage1"] = stage_dict

                stage_dict = {}

                stage_dict["route_id"] = travel_option["stage2"].route_id
                stage_dict["trip_id"] = travel_option["stage2"].trip_id
                stage_dict["route_short_name"] = travel_option["stage2"].route_short_name
                stage_dict["trip_headsign"] = travel_option["stage2"].trip_headsign
                stage_dict["start_stop_id"] = travel_option["changeover_stop_id"]
                stage_dict["dest_stop_id"] = travel_option["stage2"].dest_stop_id
                stage_dict["start_stop_id_short"] = travel_option["changeover_stop_id_short"]
                stage_dict["dest_stop_id_short"] = travel_option["stage2"].dest_stop_id_short
                stage_dict["number_stops"] = len(travel_option["stage2_subroute_stops"])
                stage_dict["departure_time"] = travel_option["stage2"].departure_time
                stage_dict["all_stops_list"] = travel_option["stage2"].all_stops_list
                stage_dict["stage_subroute_stops"] = travel_option["stage2_subroute_stops"]
                stage_dict["route_shape_points"] = travel_option["stage2"].route_shape_points
                stage_dict["stage2_subroute_shape_points"] = travel_option["stage2_subroute_shape_points"]

                route_option_dict["stage2"] = stage_dict

                data.append(route_option_dict)

    # If common trips then create direct routes with this trip
    else:
        travel_options = DirectRoutes(weather_temp, weather_rain, weather_humidity, weekday, time_specified, time_period, start_stop, dest_stop, common_trip_id_list)

        for trip in travel_options.common_trips_dict:

            # Check trip is valid
            if travel_options.common_trips_dict[trip].valid:

                route_option_dict = {}

                route_option_dict["direct"] = True
                route_option_dict["route_id"] = travel_options.common_trips_dict[trip].route_id
                route_option_dict["trip_id"] = travel_options.common_trips_dict[trip].trip_id
                route_option_dict["route_short_name"] = travel_options.common_trips_dict[trip].route_short_name
                route_option_dict["trip_headsign"] = travel_options.common_trips_dict[trip].trip_headsign
                route_option_dict["start_stop_id"] = travel_options.common_trips_dict[trip].start_stop_id
                route_option_dict["dest_stop_id"] = travel_options.common_trips_dict[trip].dest_stop_id
                route_option_dict["start_stop_id_short"] = travel_options.common_trips_dict[trip].start_stop_id_short
                route_option_dict["dest_stop_id_short"] = travel_options.common_trips_dict[trip].dest_stop_id_short
                route_option_dict["start_stop_predicted_arrival_time"] = travel_options.common_trips_dict[trip].predicted_start_arrival_time
                route_option_dict["start_stop_predicted_arrival_timestamp"] = change_to_timestamp(route_option_dict["start_stop_predicted_arrival_time"])
                route_option_dict["number_stops"] = travel_options.common_trips_dict[trip].number_stops
                route_option_dict["total_travel_time"] = travel_options.common_trips_dict[trip].total_travel_time
                route_option_dict["departure_time"] = travel_options.common_trips_dict[trip].departure_time
                route_option_dict["all_stops_list"] = travel_options.common_trips_dict[trip].all_stops_list
                route_option_dict["subroute_stops_list"] = travel_options.common_trips_dict[trip].subroute_stops_list
                route_option_dict["route_shape_points"] = travel_options.common_trips_dict[trip].route_shape_points
                route_option_dict["subroute_shape_points"] = travel_options.common_trips_dict[trip].subroute_shape_points

                data.append(route_option_dict)


    return JsonResponse({'routes_data': data})



def change_to_timestamp(datetime_time_object):
   '''
   Function that changes a datetime time object into a timestamp for todays date,
   simply used by frontend to display arrival time.
   '''

   t = datetime_time_object
   seconds = (((t.hour * 60) + t.minute) * 60) + t.second
   date_specified = datetime.datetime.now()
   date_specified = date_specified.replace(hour=0, minute=0, second=0, microsecond=0)
   timestamp = datetime.datetime.timestamp(date_specified)
   arrival_timestamp = timestamp + seconds

   return int(arrival_timestamp * 1000)



class Route():
    '''
    Superclass object that represents anytype of route between a
    start and end destination bus stop.

    Contains attributes relating to weather, date specified and bus stops.
    '''

    def __init__(self, weather_temp, weather_rain, weather_humidity, weekday, time, time_period, start_stop, dest_stop):
        self.weather_temp = weather_temp
        self.weather_rain = weather_rain
        self.weather_humidity = weather_humidity
        self.weekday = weekday
        self.time_period = time_period

        self.time = time
        time = time.split(":")
        hour = int(time[0])
        min = int(time[1])
        sec = int(time[2])
        self.time_specified = datetime.time(hour, min, sec)

        self.start_stop = start_stop
        self.dest_stop = dest_stop
        self.start_stop_id = start_stop.stop_id
        self.start_stop_id_short = start_stop.stop_id_short
        self.dest_stop_id = dest_stop.stop_id
        self.dest_stop_id_short = dest_stop.stop_id_short



class DirectRoutes(Route):
    '''
    Subclass of Route that represents a direct route between two bus stops.

    Contains an additional attribute representing the trip IDs common to both bus stops.
    '''

    def __init__(self, weather_temp, weather_rain, weather_humidity, weekday, time, time_period, start_stop, dest_stop, common_trip_ids):
        Route.__init__(self, weather_temp, weather_rain, weather_humidity, weekday, time, time_period, start_stop, dest_stop)
        self.common_trip_ids = common_trip_ids
        self.common_trips_dict = self.create_trips(self.common_trip_ids)

    def create_trips(self, common_trip_ids):
        '''
        Function that creates trip objects for each trip ID contained in the list
        Returns a dictionary of trip ID to Trip Object
        '''

        trip_dict = {}

        for trip in common_trip_ids:
            trip_dict[trip] = Trip(trip, self.weather_temp, self.weather_rain, self.weather_humidity, self.weekday, self.time, self.time_period, self.start_stop, self.dest_stop)

        return trip_dict



class MultiRoutes(Route):
    '''
    Subclass of Route that represents a multi route between two stops e.g one that
    no direct route exists

    Contains additional attributes of two lists that represent trip IDs of the start and destination
    stop respectively
    '''

    def __init__(self, weather_temp, weather_rain, weather_humidity, weekday, time, time_period, start_stop, dest_stop, start_trip_ids, dest_trip_ids):
        Route.__init__(self, weather_temp, weather_rain, weather_humidity, weekday, time, time_period, start_stop, dest_stop)
        self.start_trip_ids = start_trip_ids
        self.dest_trip_ids = dest_trip_ids
        self.start_trips_dict = self.create_start_trips(self.start_trip_ids)
        self.dest_trips_dict = self.create_dest_trips(self.dest_trip_ids)

        self.multi_trips_list = self.check_for_common_stops()


    def create_start_trips(self, trip_id_list):
        '''
        Function that creates trip objects for each trip in the list

        Returns dictionary of trip ID to trip Object
        '''

        trip_dict = {}

        for trip in trip_id_list:
            trip_dict[trip] = Trip(trip, self.weather_temp, self.weather_rain, self.weather_humidity, self.weekday, self.time, self.time_period, self.start_stop, None)

            # If arrival time is before time specified then delete
            if trip_dict[trip].valid == False:
                del trip_dict[trip]

        return trip_dict


    def create_dest_trips(self, trip_id_list):
        '''
        Function that creates trip objects for each trip in the list

        Returns dictionary of trip ID to trip Object
        '''

        trip_dict = {}

        for trip in trip_id_list:
            trip_dict[trip] = Trip(trip, self.weather_temp, self.weather_rain, self.weather_humidity, self.weekday, self.time, self.time_period, None, self.dest_stop)

        return trip_dict


    def reset_flags(self, trip_dict):
        '''
        Function that resets the "used_trip" flag for each trip in the dictionary
        provided for each iteration through the multi-route calculation algorithm
        '''

        for key in trip_dict:
            trip_dict[key].used_trip = False


    def check_for_common_stops(self):
        '''
        Function responsible for calculating that multi routing between two
        dictionarys of trip IDs. Compares each stop in each trip of the
        starting location to each stop of each trip in the destination
        location

        Contains a flag that prevents two trips from matching on more
        than one bus stop

        If a match is found a check is carried out to ensure that the second
        bus stop arrival time is greater than the first bus stop arrival time
        eg that the second bus departs after the arrival of the first bus

        The wait time between buses is limited to 40 minutes

        A counter limits this function to 5 results

        The function returns a list of dictionaries representing different
        multi-route options
        '''

        multi_trip_list = []

        options_count = 0
        self.reset_flags(self.dest_trips_dict)

        for trip_key in self.start_trips_dict:

            for stop_dict in self.start_trips_dict[trip_key].subroute_stops_list:

                for trip_key2 in self.dest_trips_dict:

                    if self.dest_trips_dict[trip_key2].used_trip == False:
                        for stop_dict2 in self.dest_trips_dict[trip_key2].subroute_stops_list:

                            if stop_dict["stop_id"] == stop_dict2["stop_id"]:
                                # Found a stop common to both trips

                                first_leg_arrival = stop_dict["predicted_arrival_time"]
                                first_leg_seconds = (first_leg_arrival.hour * 60 + first_leg_arrival.minute) * 60 + first_leg_arrival.second

                                second_leg_dept = stop_dict2["predicted_arrival_time"]
                                second_leg_seconds = (second_leg_dept.hour * 60 + second_leg_dept.minute) * 60 + second_leg_dept.second

                                wait_time_seconds = second_leg_seconds - first_leg_seconds

                                # Add in max waiting time
                                max_wait_time_seconds = 40 * 60

                                if first_leg_seconds < second_leg_seconds and wait_time_seconds < max_wait_time_seconds:

                                    common_stop_id = stop_dict["stop_id"]
                                    common_stop_id_short = stop_dict["stop_id_short"]
                                    stage1_stop_sequence = stop_dict["stop_sequence"]
                                    stage2_stop_sequence = stop_dict2["stop_sequence"]

                                    options_count += 1


                                    second_leg_arrive_dest = self.dest_trips_dict[trip_key2].predicted_dest_arrival_time
                                    second_leg_arrive_dest_seconds = (second_leg_arrive_dest.hour * 60 + second_leg_arrive_dest.minute) * 60 + second_leg_arrive_dest.second

                                    first_leg_departure = self.start_trips_dict[trip_key].predicted_start_arrival_time
                                    first_leg_departure_seconds = (first_leg_departure.hour * 60 + first_leg_departure.minute) * 60 + first_leg_departure.second

                                    total_time = second_leg_arrive_dest_seconds - first_leg_departure_seconds

                                    multi_trip_dict = {}

                                    multi_trip_dict["stages"] = 2
                                    multi_trip_dict["changeover_stop_id"] = common_stop_id
                                    multi_trip_dict["changeover_stop_id_short"] = common_stop_id_short
                                    multi_trip_dict["start_stop_predicted_arrival_time"] = self.start_trips_dict[trip_key].predicted_start_arrival_time
                                    multi_trip_dict["changeover_stop_predicted_arrival_time"] = second_leg_dept

                                    multi_trip_dict["stage1_time"] = round((first_leg_seconds - first_leg_departure_seconds)/60)
                                    multi_trip_dict["wait_time"] = round(wait_time_seconds/60)
                                    multi_trip_dict["stage2_time"] = round((second_leg_arrive_dest_seconds - second_leg_seconds)/60)
                                    multi_trip_dict["total_time"] = round(total_time/60)
                                    multi_trip_dict["stage1"] = self.start_trips_dict[trip_key]
                                    multi_trip_dict["stage2"] = self.dest_trips_dict[trip_key2]

                                    stop_and_shapes_list_stage1 = self.start_trips_dict[trip_key].get_stage_subroutes_and_shapes(stage1_stop_sequence)
                                    stop_and_shapes_list_stage2 = self.dest_trips_dict[trip_key2].get_stage_subroutes_and_shapes(stage2_stop_sequence)

                                    multi_trip_dict["stage1_subroute_stops"] = stop_and_shapes_list_stage1[1]
                                    multi_trip_dict["stage2_subroute_stops"] = stop_and_shapes_list_stage2[1]

                                    multi_trip_dict["stage1_subroute_shape_points"] = stop_and_shapes_list_stage1[0]
                                    multi_trip_dict["stage2_subroute_shape_points"] = stop_and_shapes_list_stage2[0]

                                    multi_trip_list.append(multi_trip_dict)

                                    self.dest_trips_dict[trip_key2].used_trip = True

                                    if options_count >= 5:
                                        return multi_trip_list

                                    break

            # Reset used flag for all destination trips
            self.reset_flags(self.dest_trips_dict)

        return multi_trip_list



class Trip():
    '''
    Another class that is a component of Direct Routes and MultiRoutes. It represents a
    specific trip with a specfic ID between two bus stops

    Both DirectRoutes and MultiRoutes create multiple trip objects

    Contains the same attributes as Route and its subclasses with additional
    trip specific attributes such as Headsign, shape ID, Route ID and route short name

    Contains several lists, a list of all the bus stops along the full route, a sub list of
    these stops but jsut along the route specfied, a list of all shape points and again
    a sublist of the shape points needed
    '''

    def __init__(self, trip_id, weather_temp, weather_rain, weather_humidity, weekday, time, time_period, start_stop = None, dest_stop = None):

        self.trip_id = trip_id
        self.weather_temp = weather_temp
        self.weather_rain = weather_rain
        self.weather_humidity = weather_humidity
        self.weekday = weekday
        self.time_period = time_period

        time = time.split(":")
        hour = int(time[0])
        min = int(time[1])
        sec = int(time[2])
        self.time_specified = datetime.time(hour, min, sec)

        if start_stop:
            self.start_stop = start_stop
            self.start_stop_id = start_stop.stop_id
            self.start_stop_id_short = start_stop.stop_id_short

        if dest_stop:
            self.dest_stop = start_stop
            self.dest_stop_id = dest_stop.stop_id
            self.dest_stop_id_short = dest_stop.stop_id_short

        trips_query_set = Trips.objects.filter(trip_id = self.trip_id).values_list('route_id', 'trip_headsign', 'shape_id')

        self.route_id = trips_query_set[0][0]
        self.trip_headsign = trips_query_set[0][1]
        self.shape_id = trips_query_set[0][2]
        self.route_short_name = Routes.objects.filter(route_id = self.route_id).values_list('route_short_name', flat = True)[0]

        self.all_stops_list = self.get_all_stops()

        if all(hasattr(self, attr) for attr in ["start_stop", "dest_stop"]):
            self.check_valid_stop_sequence()

        else:
            self.valid_stop_sequence = True

        # Check if valid, maybe terminate if not
        if hasattr(self, 'start_stop') :
            self.check_valid_arrival_time()

        else:
            self.valid_start_arrival_time = True

        self.check_valid()


        self.subroute_stops_list = self.get_subroute_stops()
        self.number_stops = len(self.subroute_stops_list) - 1

        self.route_shape_points = self.get_all_shape_points()
        self.subroute_shape_points = self.get_subroute_shape_points()


    def get_all_stops(self):
        '''
        Function that returns a list of stops as a dictionary object and assigns it
        to self.all_stops_list

        This dictionary contains stop name, id, lat, lng, stop_sequence, due_arrival_time,
        distance travelled and distance from previous stop

        Calculates the predicted arrival time at each bus stop by calling the
        predict function with the trip attributes
        '''

        stops = []

        stop_ids = list(MapTripStopTimes.objects.filter(trip_id = self.trip_id).values_list('stop_id','stop_sequence', 'arrival_time', 'shape_dist_traveled'))

        stop_sequence_list = list(MapTripStopTimes.objects.filter(trip_id = self.trip_id).values_list('stop_sequence', flat = True))

        self.departure_time = stop_ids[0][2]

        route_short_name = self.route_short_name
        stop_sequence_list = stop_sequence_list

        stop_seq_time_diff_dict = predict(self.weather_temp, self.weather_rain, self.weather_humidity, self.time_period, self.weekday, route_short_name, stop_sequence_list)

        for stop in stop_ids:

            stop_dict = {}
            stops_query_set = Stops.objects.filter(stop_id = stop[0]).values_list('stop_name', 'stop_lat', 'stop_lng', 'stop_id_short')

            stop_dict["stop_id"] = stop[0]
            stop_dict["stop_id_short"] = stops_query_set[0][3]
            stop_dict["stop_name"] = stops_query_set[0][0]
            stop_dict["stop_lat"] = stops_query_set[0][1]
            stop_dict["stop_lng"] = stops_query_set[0][2]
            stop_dict["stop_sequence"] = stop[1]
            stop_dict["due_arrival_time"] = stop[2]

            stop_sequence = stop[1]

            predicted_diff_in_time = stop_seq_time_diff_dict[stop_sequence]

            due_time = datetime.datetime.strptime(stop_dict["due_arrival_time"], "%H:%M:%S")
            predicted_arrival_time = (due_time + datetime.timedelta(minutes=predicted_diff_in_time)).time()
            stop_dict["predicted_arrival_time"] = predicted_arrival_time

            if hasattr(self, 'start_stop') and stop[0] == self.start_stop_id:
                self.predicted_start_arrival_time = predicted_arrival_time

            if stop[3] == None:
                previous_dist_travelled = 0
                stop_dict["shape_distance_travelled"] = 0
                stop_dict["distance_from_previous"] = 0

            else:
                stop_dict["shape_distance_travelled"] = stop[3]
                stop_dict["distance_from_previous"] = stop[3] - previous_dist_travelled

            if hasattr(self, 'start_stop') and stop[0] == self.start_stop_id:
                self.start_stop_sequence = stop[1]

                if stop[3] == None:
                    self.start_stop_distance = 0
                else:
                    self.start_stop_distance = stop[3]

            if hasattr(self, 'dest_stop') and stop[0] == self.dest_stop_id:
                self.predicted_dest_arrival_time = predicted_arrival_time
                self.dest_stop_sequence = stop[1]

                if stop[3] == None:
                    self.dest_stop_distance = 0
                else:
                    self.dest_stop_distance = stop[3]

            previous_dist_travelled = stop_dict["shape_distance_travelled"]

            stops.append(stop_dict)

        if all(hasattr(self, attr) for attr in ["start_stop", "dest_stop"]):

            predicted_start_arrival_time_seconds = (self.predicted_start_arrival_time.hour * 60 + self.predicted_start_arrival_time.minute) * 60 + self.predicted_start_arrival_time.second

            predicted_dest_arrival_time_seconds = (self.predicted_dest_arrival_time.hour * 60 + self.predicted_dest_arrival_time.minute) * 60 + self.predicted_dest_arrival_time.second

            total_travel_time = (predicted_dest_arrival_time_seconds - predicted_start_arrival_time_seconds)/60

            self.total_travel_time = total_travel_time

        return stops


    def get_subroute_stops(self):
        '''
        Function that creates a list of subroute bus stops depending on
        the type of trip object eg first leg, second leg or direct route

        Returns a list of dictionaries
        '''
        stops = []

        # Check which type of subroute is needed
        # Has start and dest stop IDs e.g Direct Route
        if all(hasattr(self, attr) for attr in ["start_stop", "dest_stop"]):

            end_stop_order = max(self.start_stop_sequence, self.dest_stop_sequence)
            start_stop_order = min(self.start_stop_sequence, self.dest_stop_sequence)

            for stop_dict in self.all_stops_list:
                stop_sequence = stop_dict["stop_sequence"]

                if stop_sequence <= end_stop_order and stop_sequence >= start_stop_order:
                    stops.append(stop_dict)

        # Has just start stop ID specfied, start to end subroute
        elif hasattr(self, 'start_stop'):

            for stop_dict in self.all_stops_list:
                stop_sequence = stop_dict["stop_sequence"]

                if stop_sequence >= self.start_stop_sequence:
                    stops.append(stop_dict)

        # Has just dest ID specified, all to dest subroute
        elif hasattr(self, 'dest_stop'):

            for stop_dict in self.all_stops_list:
                stop_sequence = stop_dict["stop_sequence"]

                if stop_sequence <= self.dest_stop_sequence:
                    stops.append(stop_dict)

        return stops


    def check_valid_stop_sequence(self):
        '''
        Checks that the start stop has lower stop sequence then
        destination else it is invalid
        '''

        if self.start_stop_sequence < self.dest_stop_sequence:
            self.valid_stop_sequence = True

        else:
            self.valid_stop_sequence = False


    def check_valid_arrival_time(self):
        '''
        Checks that the bus arrival time to start bus stop is less
        than that specified by the user else invalid
        '''

        if self.predicted_start_arrival_time > self.time_specified:
            self.valid_start_arrival_time = True

        else:
            self.valid_start_arrival_time = False

    def check_valid(self):
        '''
        Checks that both arrival time and stop sequence are valid
        '''

        if self.valid_stop_sequence == True and self.valid_start_arrival_time == True:
            self.valid = True

        else:
            self.valid = False


    def get_all_shape_points(self):
        '''
        Function that returns all the shape points for a route
        '''

        shape_points = list(Shapes.objects.filter(shape_id = self.shape_id).values('shape_point_sequence', 'shape_point_lat', 'shape_point_lng', 'shape_dist_travelled'))

        return shape_points


    def get_subroute_shape_points(self):
        '''
        Function that creates a list of sub route shape points

        Returns a list of shape poin=t dictionaries
        '''

        shape_points = []

        if all(hasattr(self, attr) for attr in ["start_stop", "dest_stop"]):

            for point in self.route_shape_points:

                if point["shape_dist_travelled"] == self.start_stop_distance:
                    start_seq = point["shape_point_sequence"]
                elif point["shape_dist_travelled"] == self.dest_stop_distance:
                    dest_seq = point["shape_point_sequence"]

            max_seq = max(start_seq, dest_seq)
            min_seq = min(start_seq, dest_seq)

            for point in self.route_shape_points:
                shape_seq = point["shape_point_sequence"]

                if shape_seq >= min_seq and shape_seq <= max_seq:
                    shape_points.append(point)


        elif hasattr(self, 'start_stop'):
            for point in self.route_shape_points:

                if point["shape_dist_travelled"] == self.start_stop_distance:
                    start_seq = point["shape_point_sequence"]
                    break

            for point in self.route_shape_points:
                shape_seq = point["shape_point_sequence"]

                if shape_seq >= start_seq:
                    shape_points.append(point)

        elif hasattr(self, 'dest_stop'):
            for point in self.route_shape_points:

                if point["shape_dist_travelled"] == self.dest_stop_distance:
                    end_seq = point["shape_point_sequence"]
                    break

            for point in self.route_shape_points:
                shape_seq = point["shape_point_sequence"]

                if shape_seq <= end_seq:
                    shape_points.append(point)

        return shape_points


    def get_stage_subroute_shape_points(self, common_stop_distance):
        '''
        Function similar to the get_subroute_shape_points that returns a subroute
        of shape points based on the common bus stop for a multi-route

        Returns a list of shape points dictionaries
        '''

        shape_points = []

        if hasattr(self, 'start_stop'):
            for point in self.subroute_shape_points:

                if point["shape_dist_travelled"] == common_stop_distance:
                    seq = point["shape_point_sequence"]
                    break

            for point in self.subroute_shape_points:
                shape_seq = point["shape_point_sequence"]

                if shape_seq <= seq:
                    shape_points.append(point)

        elif hasattr(self, 'dest_stop'):
            for point in self.subroute_shape_points:

                if point["shape_dist_travelled"] == common_stop_distance:
                    seq = point["shape_point_sequence"]
                    break

            for point in self.subroute_shape_points:
                shape_seq = point["shape_point_sequence"]

                if shape_seq >= seq:
                    shape_points.append(point)

        return shape_points


    def get_stage_subroutes_and_shapes(self, common_stop_sequence):
        '''
        Function similar to the get_subroute_stops
        Uses the get_stage_subroute_shape_points function to creat a
        list of shape points for this subroute

        Returns a list of two lists, one for shape points and one
        for bus stops, both are dictionaries
        '''

        stop_and_shapes_list = []
        stops = []

        # Check which type of stage_subroute is needed
        # Has just start stop ID specfied, start to end subroute
        if hasattr(self, 'start_stop'):

            for stop_dict in self.subroute_stops_list:
                stop_sequence = stop_dict["stop_sequence"]

                if stop_sequence == common_stop_sequence:

                    common_stop_distance = stop_dict["shape_distance_travelled"]
                    shapes = self.get_stage_subroute_shape_points(common_stop_distance)
                    stop_and_shapes_list.append(shapes)

                if stop_sequence <= common_stop_sequence:
                    stops.append(stop_dict)

        # Has just dest ID specified, all to dest subroute
        elif hasattr(self, 'dest_stop'):

            for stop_dict in self.subroute_stops_list:
                stop_sequence = stop_dict["stop_sequence"]

                if stop_sequence == common_stop_sequence:

                    common_stop_distance = stop_dict["shape_distance_travelled"]
                    shapes = self.get_stage_subroute_shape_points(common_stop_distance)
                    stop_and_shapes_list.append(shapes)

                if stop_sequence >= common_stop_sequence:
                    stops.append(stop_dict)

        stop_and_shapes_list.append(stops)

        return stop_and_shapes_list



def predict(weather_temp, weather_rain, weather_humidity, time_period, weekday, route_short_name, stop_sequence_list):
    '''
    Predict function that calculates the prediction of arrival times for each
    bus stop along a route

    Loads the SGD model from a SAV file

    Returns a dictionary of bus stop sequence number as key and the
    variance in arrival time as the value

    eg sequence 16: +20seconds
    '''

    route_short_name = route_short_name
    stop_stop_sequence_list = stop_sequence_list
    sequence_time_diff_dict = {}

    line_list= ['75', '68X', '13', '41A', '46E', '104', '7A', '18', '32', '25A', '38A', '76',
                '33B', '14C', '37', '33E', '9', '4', '70D', '15B', '56A', '65B', '140', '67X',
                '68A', '66', '61', '33X', '31', '11', '114', '43', '41D', '130', '51X', '49',
                 '69', '41X', '7', '15', '122', '40', '31D', '27A', '40D', '111', '25D', '54A',
                 '116', '145', '7D', '76A', '17', '15A', '38B', '185', '120', '45A', '83A',
                 '25B', '38D', '84', '63', '17A', '16D', '70', '15D', '32X', '41B', '39',
                 '84X', '25', '14', '31B', '77A', '79', '66X', '33A', '31A', '38', '84A',
                 '238', '68', '236', '16C', '220', '161', '27X', '46A', '33', '102', '41C',
                 '53', '27', '151', '66B', '42', '67', '142', '40E', '150', '47', '270', '44B',
                 '65', '239', '40B', '44', '59', '7B', '79A', '77X', '33D', '184', '39X', '1',
                 '51D', '42D', '29A', '83', '69X', '39A', '41', '27B', '66A', '16', '25X', '26',
                 '118', '123']

    file = 'map/pickles/SGD_original_model.sav'
    da_model = joblib.load(file)

    try:
        binary="{0:08b}".format(line_list.index(route_short_name))
        numbers=list(binary)
        numbers = [int(x) for x in numbers]

        dataframe = pd.DataFrame(columns=('progr_number',  'rain', 'temp', 'rhum', 'Time_period', 'weekday', 'Col_1', 'Col_2', 'Col_3', 'Col_4', 'Col_5', 'Col_6', 'Col_7', 'Col_8'))
        features = ['progr_number',  'rain', 'temp', 'rhum', 'Time_period', 'weekday', 'Col_1', 'Col_2', 'Col_3', 'Col_4', 'Col_5', 'Col_6', 'Col_7', 'Col_8']

        for i in range(len(stop_stop_sequence_list)):
            dataframe.loc[i] = [stop_stop_sequence_list[i], weather_rain, weather_temp, weather_humidity, 2, weekday, numbers[0], numbers[1], numbers[2], numbers[3], numbers[4], numbers[5], numbers[6], numbers[7]]

    except:
        # Backup Model
        dataframe = pd.DataFrame(columns=('progr_number',  'rain', 'temp', 'rhum', 'Time_period', 'weekday', 'Col_1', 'Col_2', 'Col_3', 'Col_4', 'Col_5', 'Col_6', 'Col_7', 'Col_8'))
        features = ['progr_number',  'rain', 'temp', 'rhum', 'Time_period', 'weekday', 'Col_1', 'Col_2', 'Col_3', 'Col_4', 'Col_5', 'Col_6', 'Col_7', 'Col_8']

        for i in range(len(stop_stop_sequence_list)):
            dataframe.loc[i] = [stop_stop_sequence_list[i], weather_rain, weather_temp, weather_humidity, 2, weekday, 0, 0, 0, 0, 0, 0, 0, 0]

    finally:
        time_dif_list = da_model.predict(dataframe[features])

        for i in range(len(time_dif_list)):
            sequence_time_diff_dict[stop_stop_sequence_list[i]] = time_dif_list[i]

        return sequence_time_diff_dict



def get_current_weather():
    '''
    Function that returns a list of the current weather
    Connects to database where the data is stored

    Returns temperature, rain and humidity
    '''

    try:
        params = {
            'database': 'weather',
            'user': 'student',
            'password': 'group10bus',
            'host': 'localhost',
            'port': 3333
            }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()

        curs.execute("SELECT weather_temp, weather_rain, weather_humidity from current_weather;")
        rows = curs.fetchall()

        weather_temp = rows[0][0]
        weather_rain = rows[0][1]
        weather_humidity = rows[0][2]

        if(conn):
            curs.close()
            conn.close()

    except:
        weather_temp = 15
        weather_rain = 0
        weather_humidity = 80

    return [weather_temp, weather_rain, weather_humidity]



def get_weather_forecast(datetime_object):
    '''
    Function that returns a list of the weather forecast for a specfied
    date and time
    Connects to database where the data is stored

    Returns temperature, rain and humidity

    Has Backup weather in case forecast is unavailable
    '''

    params = {
        'database': 'weather',
        'user': 'student',
        'password': 'group10bus',
        'host': 'localhost',
        'port': 3333
        }

    conn = psycopg2.connect(**params)
    curs = conn.cursor()
    date_string = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
    date_timestamp = datetime_object.timestamp()

    query = "SELECT  weather_temp, weather_rain, weather_humidity, timestamp FROM weather_forecast ORDER BY abs(extract(epoch from (timestamp - timestamp '" + date_string + "'))) LIMIT 1;"
    curs.execute(query)
    rows = curs.fetchall()

    latest_data_timestamp = (rows[0][3]).timestamp()

    # If latest weather is less than 3 hours then use it
    if abs(latest_data_timestamp - date_timestamp) < 10800:
        weather_temp = rows[0][0]
        weather_rain = rows[0][1]
        weather_humidity = rows[0][2]

    #Backup weather
    else:
        weather_temp = 15
        weather_rain = 0
        weather_humidity = 80

    if(conn):
        curs.close()
        conn.close()

    return [weather_temp, weather_rain, weather_humidity]



def get_time_period(specified_date_time):
    '''
    Function that turns a specified time into a time period bin
    that will be used with the predictive model

    Returns an integer between 0 and 6
    '''

    seconds =(specified_date_time.hour * 60 + specified_date_time.minute) * 60 + specified_date_time.second

    if seconds >= 0 and seconds < 25200:
        return 0
    elif seconds >= 25200 and seconds < 36000:
        return 5
    elif seconds >= 36000 and seconds < 54000:
        return 3
    elif seconds >= 54000 and seconds < 61200:
        return 4
    elif seconds >= 61200 and seconds < 68400:
        return 6
    elif seconds >= 68400 and seconds < 79200:
        return 2
    elif seconds >= 79200:
        return 1
