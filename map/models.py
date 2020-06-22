from django.db import models

class Routes(models.Model):

    route_id = models.CharField(primary_key = True, verbose_name = "Route ID", max_length=100)
    agency_id = models.CharField(verbose_name = "Agency associated with data", max_length=20)
    route_short_name = models.CharField(verbose_name = "Line ID", max_length=20)

class Stops(models.Model):

    stop_id = models.CharField(primary_key = True, verbose_name = "Bus stop ID", max_length = 100)
    stop_id_short = models.IntegerField(verbose_name = "Short Bus stop ID")
    stop_name = models.CharField(verbose_name = "Stop Name", max_length = 200)
    stop_lat = models.FloatField(verbose_name = "Stop Latitude")
    stop_lng = models.FloatField(verbose_name = "Stop Longitude")

class CalendarService(models.Model):

    service_id = models.CharField(primary_key = True, verbose_name = "Service ID for specific days and dates", max_length = 100)
    start_date = models.DateField(verbose_name = "Start date of this service schedule")
    end_date = models.DateField(verbose_name = "Planned end date for this service schedule I think, possibly redundant.")
    monday = models.BooleanField(verbose_name = "Serviced on this day")
    tuesday = models.BooleanField(verbose_name = "Serviced on this day")
    wednesday = models.BooleanField(verbose_name = "Serviced on this day")
    thursday = models.BooleanField(verbose_name = "Serviced on this day")
    friday = models.BooleanField(verbose_name = "Serviced on this day")
    saturday = models.BooleanField(verbose_name = "Serviced on this day")
    sunday = models.BooleanField(verbose_name = "Serviced on this day")

class CalendarExceptions(models.Model):

    service_id = models.ForeignKey("CalendarService", on_delete=models.CASCADE, verbose_name = "Service ID from calendar table")
    exception_date = models.DateField(verbose_name = "Date of exception")
    exception_type = models.IntegerField(verbose_name = "Type of exception, no info on types")

    class Meta:
        unique_together = ('service_id', 'exception_date')

class Shapes(models.Model):

    shape_id = models.CharField(verbose_name = "Identifies a shape", max_length = 100)
    shape_point_lat = models.FloatField(verbose_name = "Shape Point Latitude")
    shape_point_lng = models.FloatField(verbose_name = "Shape Point Longitude")
    shape_point_sequence = models.IntegerField(verbose_name = "Point sequence along shape")
    shape_dist_travelled = models.FloatField(verbose_name = "Distance travelled so far to this point")

    class Meta:
        unique_together = ('shape_id', 'shape_point_sequence')

class Trips(models.Model):

    trip_id = models.CharField(primary_key = True, verbose_name = "Unique trip ID that represents a route, time of day, direction and specific calendar schedule", max_length = 100)
    route_id = models.ForeignKey("Routes", on_delete=models.CASCADE, verbose_name = "Route ID from Routes")
    direction = models.BooleanField(verbose_name = "Indicates direction for bidirectional route_ids")
    trip_headsign = models.CharField(verbose_name = "Headsign to be used when no headsign change mid trip", max_length = 200)
    shape_id = models.CharField(verbose_name = "Should be a FK for Shapes but shape id is not unique", max_length = 100)
    service_id = models.ForeignKey("CalendarService", on_delete=models.CASCADE, verbose_name = "Identifies the service schedule for this trip eg what days of week operational")


#Insert Here Model from inspectDB


class MapTripStopTimes(models.Model):

    trip = models.ForeignKey('Trips', models.CASCADE, primary_key=True)
    stop = models.ForeignKey('Stops', models.CASCADE)
    stop_sequence = models.IntegerField()
    arrival_time = models.TextField(blank=True, null=True)
    departure_time = models.TextField(blank=True, null=True)
    stop_headsign = models.CharField(max_length=200, blank=True, null=True)
    shape_dist_traveled = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'map_trip_stop_times'
        unique_together = (('trip', 'stop', 'stop_sequence'),)
