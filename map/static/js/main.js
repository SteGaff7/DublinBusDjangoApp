//Primary JavaScript



//Get the local URL
var getUrl = window.location;
//Set the format of URL
var map_Url = getUrl.protocol + "//" + getUrl.host + "/";

function getFare() {
    $('.details').css('display','none');
    $('#showFare').css('display','block');
}


//Show or hide startjourney button of mobile device
function showStartJourney() {
    var browserWidth = document.body.clientWidth;
    if (browserWidth < 767) {
       $("#startjourney").show(); 
    }
    
}
//Hide loading
function hideStartJourney() {
    var browserWidth = document.body.clientWidth;
    if (browserWidth < 767) {
       $("#startjourney").hide();
    }
}
 
 //Convert the timestamp to normal time and only show hour and minute     
 function getLocalTime(timeStamp) {  
 var minuteFormat = function(minuteNumber){return minuteNumber < 10 ? '0' + minuteNumber : minuteNumber};
 return minuteFormat(new Date(parseInt(timeStamp)).getHours()) + ":" + minuteFormat(new Date(parseInt(timeStamp)).getMinutes());
}
 //Code here reference from part of a template and was changed to fit this project   
 (function ($) {
     $(document).ready(function () {
         $('.menuToggle').click(function (e) {
             $('#menuToggleIcon').css('display','block');
             var $parent = $('.menuToggle').parent('nav');
             $parent.toggleClass("open");
             $(this).attr("Go Back");
             e.preventDefault();
         });
     });
 })(jQuery);


 (function ($) {
     $(document).ready(function () {
         $('#menuToggleIcon').click(function (e) {
            $('#menuToggleIcon').css('display','none');
             e.preventDefault();
         });
     });
 })(jQuery);



      


//Show loading icon
function ShowDiv() {
    var browserWidth = document.body.clientWidth;
    if (browserWidth >= 767) {
       $("#loading").show();
       $("#loading_2").hide();
       $("#loading_icon").hide();
    }
    else {
    document.getElementById('loading_icon').src = document.getElementById('loading_icon').src;
    $("#loading_2").show();
    $("#loading_icon").show();
    $("#loading").hide();
}
}
//Hide loading icon
function HiddenDiv() {
    var browserWidth = document.body.clientWidth;
    if (browserWidth >= 767) {
       $("#loading").hide();
       $("#loading_2").hide();
       $("#loading_icon").hide();
    }
    else { 
    document.getElementById('loading_icon').src = document.getElementById('loading_icon').src;
       $("#loading").hide();
       $("#loading_2").hide();
       $("#loading_icon").hide();
    }
}


//A function to add 0 before a number if it is less than 10
function addZero(e) {
    if (e < 10) {
    return '0' + e
    }
    else {
    return e
    }
}  
    

//Get the date today as a format like mm/dd/yy
function getMonthDayYear() {
    var newData = new Date();
    var todayYear = String(newData.getFullYear())[2] + String(newData.getFullYear())[3];
    var todayMonth = newData.getMonth() + 1;
    var monthFormat = addZero(todayMonth)
    var todayDay = String(newData.getDate());
    var finalDateToday = monthFormat + "/" + todayDay + "/" + todayYear;
    
    return finalDateToday
    
}  



//Hide time and data pickers when the time to go is chosen as "Now", and show them when "Later" is chosen.
function hideTimeAndDataPicker() {
    if ($('#timediv').css("display") == "none" && $('#datediv').css("display") == "none") {
        $("#timediv").show();
        $("#datediv").show();
    } else {
        $("#timediv").hide();
        $("#datediv").hide();
        $(".timepicker").val("");
        $(".datepicker").val("");
    }
}

    
    
// Get the details of a selected row in the table    
$(".details").on("click",".routeOptions",function(e){
    
    // Setting interaction for mobile version
    $('#menuToggleIcon').css('display','none');
    var $parent = $('.menuToggle').parent('nav');
    $parent.toggleClass("open");
    $(this).attr("Go Back");
    // End of mobile version design
    
    
    hideStartJourney();
    var td = $(this).find("td");
    
    if (td.eq(4).text() == "NowSingle") {
        $("#NowSingle").css('display','block');
        $("#NowMultiple").css('display','none'); 
        $("#LaterSingle").css('display','none'); 
        $("#LaterMultiple").css('display','none'); 
        
		var arrivalTime = td.eq(0).text();
        var journeyTime = td.eq(1).text();
        var allRoutes = td.eq(2).text();
        var stopNumber = td.eq(5).text();
        var li = $("#NowSingle ul").find("li");
        
        li.eq(0).html("Route: " + allRoutes);
        li.eq(1).html("Stop Number: " + stopNumber + " stops");
        li.eq(2).html("Arrives In: " + arrivalTime);
        li.eq(3).html("Estimate Journey Time: " + journeyTime);
        $("#NowSingle").css('display','block'); 
    }
    else if (td.eq(4).text() == "NowMultiple") {
        $("#NowMultiple").css('display','block');
        $("#NowSingle").css('display','none'); 
        $("#LaterSingle").css('display','none'); 
        $("#LaterMultiple").css('display','none'); 
        
		var arrivalTime = td.eq(0).text();
        var journeyTime = td.eq(1).text();
        var allRoutes = td.eq(2).text();
        var transferStopId = td.eq(5).text();
        var stage1StopNumber = td.eq(6).text();
        var stage2StopNumber = td.eq(7).text();
        var waitTime = td.eq(8).text();
        var li = $("#NowMultiple ul").find("li");
        
        li.eq(0).html("Route: " + allRoutes);
        li.eq(1).html("Transfer Stop: " + transferStopId);
        li.eq(2).html("Stage 1 Stop Number: " + stage1StopNumber + " stops");
        li.eq(3).html("Stage 2 Stop Number: " + stage2StopNumber + " stops");
        li.eq(4).html("Arrives In: " + arrivalTime);
        li.eq(5).html("Estimate Transfer Time: " + waitTime);
        li.eq(6).html("Estimate Journey Time: " + journeyTime);
        $("#NowMultiple").css('display','block'); 
    }
        else if (td.eq(4).text() == "LaterSingle") {
            
        $("#NowMultiple").css('display','none');
        $("#NowSingle").css('display','none'); 
        $("#LaterSingle").css('display','block'); 
        $("#LaterMultiple").css('display','none'); 
        
		var arrivalTime = td.eq(0).text();
        var journeyTime = td.eq(1).text();
        var allRoutes = td.eq(2).text();
        var stopNumber = td.eq(5).text();
        var li = $("#LaterSingle ul").find("li");

        li.eq(0).html("Route: " + allRoutes);
        li.eq(1).html("Stop Number: " + stopNumber + " stops");
        li.eq(2).html("Departure Time: " + arrivalTime);
        li.eq(3).html("Estimate Journey Time: " + journeyTime);
        $("#LaterSingle").css('display','block'); 
    }
        else if (td.eq(4).text() == "LaterMultiple") {
        
        $("#NowMultiple").css('display','none');
        $("#NowSingle").css('display','none'); 
        $("#LaterSingle").css('display','none'); 
        $("#LaterMultiple").css('display','block'); 
        
		var arrivalTime = td.eq(0).text();
        var journeyTime = td.eq(1).text();
        var allRoutes = td.eq(2).text();
        var transferStopId = td.eq(5).text();
        var stage1StopNumber = td.eq(6).text();
        var stage2StopNumber = td.eq(7).text();
        var waitTime = td.eq(8).text();
        var li = $("#LaterMultiple ul").find("li");
        
        li.eq(0).html("Route: " + allRoutes);
        li.eq(1).html("Transfer Stop: " + transferStopId);
        li.eq(2).html("Stage 1 Stop Number: " + stage1StopNumber + " stops");
        li.eq(3).html("Stage 2 Stop Number: " + stage2StopNumber + " stops");
        li.eq(4).html("Departure Time: " + arrivalTime);
        li.eq(5).html("Estimate Transfer Time: " + waitTime);
        li.eq(6).html("Estimate Journey Time: " + journeyTime);
        $("#LaterMultiple").css('display','block'); 
    }
        $(".details").css('display','none'); 
        $(".detailForRoute").css('display','block'); 
   });


    


//Submit the location of start and destination based on stopID and then the routes will be shown on the map
$('.searchInformation').click(function() {
    
    $(".details").html("")
    $(".detailForRoute").css('display','none'); 
    $(".details").css('display','block'); 
    

    var start_stop_code = $('#startInput').val().substring($('#startInput').val().indexOf("(Stop") + 6, $('#startInput').val().length - 1);
    var end_stop_code = $('#destitationInput').val().substring($('#destitationInput').val().indexOf("(Stop") + 6, $('#destitationInput').val().length - 1);
    var startstop = parseInt(start_stop_code);
    var endstop = parseInt(end_stop_code);
    var time_specified = $(".timepicker").val();
    var date_specified = $(".datepicker").val();
    var timeToGo = $(".nowOrLater").val();
    var infoWindow = new google.maps.InfoWindow();
    var latlngbounds = new google.maps.LatLngBounds();
    var myDate = new Date();
    var mytime = myDate.getTime();
    var checkDay = getMonthDayYear();
    var informationTable = "<table id='myTable'>";


    // Check if the search bar is empty
    if ($("#startInput").val() == '' || $("#startInput").val() == undefined || $("#startInput").val() == null || $("#destitationInput").val() == '' || $("#destitationInput").val() == undefined || $("#destitationInput").val() == null) {
        alert("Start or destination can not be empty!")
        return false
    }

    // Check if the timepicker is empty
    if (timeToGo == 'Later' && (time_specified == '' || time_specified == undefined || time_specified == null)) {
        alert("Time can not be empty!")
        return false
    }
    
    
    //Check the time selected for today is not earlier than current time
    if (date_specified == undefined || date_specified == null || date_specified == ''|| date_specified == checkDay) {
    if ((Number(getLocalTime(mytime)[0] + getLocalTime(mytime)[1]) > Number(time_specified[0] + time_specified[1])) || ((Number(getLocalTime(mytime)[0] + getLocalTime(mytime)[1]) == Number(time_specified[0] + time_specified[1]))) && ((Number(getLocalTime(mytime)[3] + getLocalTime(mytime)[4]) > Number(time_specified[3] + time_specified[4])))) {
        alert("Cannot set time before current time!")
        return false
        }
    }
    
    
    if (timeToGo != 'Later') {                         
        informationTable += "<thead><tr class='headRow'><th style = 'width: 20%'>Arrives In</th><th style = 'width: 20%'>Time</th><th style = 'width: 40%'>Route</th><th style = 'width: 20%'>Fare</th></tr></thead>";
    }

    else {
        informationTable += "<thead><tr class='headRow'><th style = 'width: 20%'>Arrives At</th><th style = 'width: 20%'>Time</th><th style = 'width: 40%'>Route</th><th style = 'width: 20%'>Fare</th></tr></thead>";   
    }

    //Ajax, get information from the specific url
    $.ajax({
        url: map_Url + "routes",
//        async: false,
        async: true,
        beforeSend: function () {
            ShowDiv();
        },
        complete: function () {
            HiddenDiv();
        },
        data: {
            startstop: startstop,
            endstop: endstop,
            time_specified: time_specified,
            date_specified: date_specified
        },
        success: function(result) {
            var MapOption = {
                center: {
                    lat: 53.350140,
                    lng: -6.266155
                },
                zoom: 14,
                mapTypeId: google.maps.MapTypeId.ROADMAP,
                gestureHandling: "greedy"
            };
            var map = new google.maps.Map(document.getElementById('map'), MapOption);
            var markersset = [];
            var markersset1 = [];
            var markersset2 = [];
            var commonroutes = result.routes_data;
            var pathArray = [];
            var pathArray1 = [];
            var pathArray2 = [];
            var BusPath;
            var BusPath1;
            var BusPath2;
            
            
            // A statement to judge if the user gets the result
            if (commonroutes.length == 0) {
                $(".details").html("");
                $("#noResult").show();
                setTimeout(function() {
                    $("#noResult").hide();;
                }, 3000); //Set the div disappeared after 3 seconds
                return false
            }
            
            for (let i = 0; i < commonroutes.length; i++) {
                        if (commonroutes[i].direct == true) {

                        //Calculate the fare of different routes based on number of stops
                        if (commonroutes[i].number_stops >= 1 && commonroutes[i].number_stops <= 3) {
                            var Adult_Cash = "€2.15";
                            var Adult_Leap = "€1.55";
                            var Child_Cash_16 = "€1.30";
                            var Child_Leap_19 = "€1.00";
                        }
                        else if (commonroutes[i].number_stops > 3 && commonroutes[i].number_stops <= 13) {
                            var Adult_Cash = "€2.25";
                            var Adult_Leap = "€2.00";
                            var Child_Cash_16 = "€1.30";
                            var Child_Leap_19 = "€1.00";

                        }
                        else {
                            var Adult_Cash = "€3.30";
                            var Adult_Leap = "€2.50";
                            var Child_Cash_16 = "€1.30";
                            var Child_Leap_19 = "€1.00";
                        }
                            
                    window.showMoney = function() {
                        var fareLi = $("#showFare").find("p");
                        fareLi.eq(0).html("\&nbsp\&nbspAdult (Cash): " + Adult_Cash);
                        fareLi.eq(1).html("\&nbsp\&nbspAdult (Leap Card): " + Adult_Leap);
                        fareLi.eq(2).html("\&nbsp\&nbspChild Under 16 (Cash): " + Child_Cash_16);
                        fareLi.eq(3).html("\&nbsp\&nbspChild Under 19 (Leap Card): " + Child_Leap_19);
                        $('tr').removeClass('routeOptions'); 
                    }

                    if (timeToGo != 'Later') {
                        if (Math.round((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) == 0) {
                            
                        informationTable += "<tbody id='myTable1'><tr class='routeOptions'><td style = 'width: 20%'>" + "Due" + "</td><td style = 'width: 20%'>" + Math.round(((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) + commonroutes[i].total_travel_time) + " mins" + "</td><td style = 'width: 40%'>" + commonroutes[i].route_short_name + "</td><td style = 'width: 20%; color:#5af542' class='exceptTd'><a style='cursor:hand' onclick=\"getFare(); showMoney()\">Show</a></td><td style='display: none'>NowSingle</td><td style='display: none'>" + commonroutes[i].number_stops + "</td></tr></tbody>";
                        }
                        
                        else {
                        
                        informationTable += "<tbody id='myTable1'><tr class='routeOptions'><td style = 'width: 20%'>" + Math.round((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) + " mins" + "</td><td style = 'width: 20%'>" + Math.round(((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) + commonroutes[i].total_travel_time) + " mins" + "</td><td style = 'width: 40%'>" + commonroutes[i].route_short_name + "</td><td style = 'width: 20%; color:#5af542' class='exceptTd'><a style='cursor:hand' onclick=\"getFare(); showMoney()\">Show</a></td><td style='display: none'>NowSingle</td><td style='display: none'>" + commonroutes[i].number_stops + "</td></tr></tbody>";  
                        }
                    }


                    else {
                        
                        informationTable += "<tbody><tr class='routeOptions'><td style = 'width: 20%'>" + getLocalTime(commonroutes[i].start_stop_predicted_arrival_timestamp) + "</td><td style = 'width: 20%'>" + Math.round(commonroutes[i].total_travel_time) + " mins" + "</td><td style = 'width: 40%'>" + commonroutes[i].route_short_name + "</td><td style = 'width: 20%; color:#5af542'><a style='cursor:hand' onclick=\"getFare(); showMoney()\">Show</a></td><td style='display: none'>LaterSingle</td><td style='display: none'>" + commonroutes[i].number_stops + "</td></tr></tbody>";       
                    }
                         
                        //Show corresponding route based on the option a user selected
                        $(".details").on("click",".routeOptions",function(e){
                         var tdMapShow = $(this).find("td");   
                         var busSeleted = tdMapShow.eq(2).text();
                         
                        if (busSeleted == commonroutes[i].route_short_name) {
                        for (var p = 0; p < markersset.length; p++) {
                            markersset[p].setMap(null);
                        }
                        markersset = [];
                            
                        if (BusPath && BusPath.setMap) {
                            BusPath.setMap(null);
                        }
                        pathArray = [];
                            
                        for (var j = 0; j < commonroutes[i].subroute_stops_list.length; j++) {
                        var get_all_stops_list = commonroutes[i].subroute_stops_list[j];
                        var routeLat = get_all_stops_list.stop_lat;
                        var routeLng = get_all_stops_list.stop_lng;
                        var myLatlng = {
                            lat: routeLat,
                            lng: routeLng
                        };

                        var marker = new google.maps.Marker({
                            position: myLatlng,
                            map: map,
                            icon: "https://img.icons8.com/ios-glyphs/30/000000/map-pin.png",
                        });
                            
                        markersset.push(marker);
                            
                        (function(marker,get_all_stops_list) {
                            google.maps.event.addListener(marker, "click", function(e) {
                                infoWindow.setContent("<div style = 'width: 200px; min-height: 40px; font-style: italic; font-weight: 800'>" + "Stop ID: " + get_all_stops_list.stop_id_short + "<br>" + "Address: " + get_all_stops_list.stop_name + "<br>" + "Sequence Number: " + get_all_stops_list.stop_sequence + "</div>");
                                infoWindow.open(map, marker);
                            });
                        })(marker,get_all_stops_list);
                        latlngbounds.extend(marker.position);
                            

                         var bounds = new google.maps.LatLngBounds();
                         map.setCenter(latlngbounds.getCenter());
                         map.fitBounds(latlngbounds);    
                        }//end of for loop
                            
                    for (var k = 0; k < commonroutes[i].subroute_shape_points.length; k++) {
                        var shapeLat = commonroutes[i].subroute_shape_points[k].shape_point_lat;
                        var shapeLng = commonroutes[i].subroute_shape_points[k].shape_point_lng;
                        var shapeLatLng = {
                            lat: shapeLat,
                            lng: shapeLng
                        };
                        pathArray[k] = shapeLatLng;
                    }
                            
                    //Draw polylines between bus stops based on their order
                    BusPath = new google.maps.Polyline({
                        path: pathArray,
                        geodesic: true,
                        strokeColor: '#D95C00',
                        strokeOpacity: 1.0,
                        strokeWeight: 4
                    });
                        BusPath.setMap(map);                
                      } //end of if loop      
                    })
                } //endif loop without transfer
              else { //start of trip with transfer

                    var transferStop = commonroutes[i].changeover_stop_id_short;


                    //Calculate the fare of different routes based on number of stops
                    if (commonroutes[i].stage1.number_stops >= 1 && commonroutes[i].stage1.number_stops <= 3) {
                        var Adult_Cash_1 = 2.15;
                        var Adult_Leap_1 = 1.55;
                        var Child_Cash_16_1 = 1.30;
                        var Child_Leap_19_1 = 1.00;
                    }
                    else if (commonroutes[i].stage1.number_stops > 3 && commonroutes[i].stage1.number_stops <= 13) {
                        var Adult_Cash_1 = 2.25;
                        var Adult_Leap_1 = 2.00;
                        var Child_Cash_16_1 = 1.30;
                        var Child_Leap_19_1 = 1.00;
                    }
                    else {
                        var Adult_Cash_1 = 3.30;
                        var Adult_Leap_1 = 2.50;
                        var Child_Cash_16_1 = 1.30;
                        var Child_Leap_19_1 = 1.00;
                    }

                     //Calculate the fare of different routes based on number of stops
                    if (commonroutes[i].stage2.number_stops >= 1 && commonroutes[i].stage2.number_stops <= 3) {
                        var Adult_Cash_2 = 2.15;
                        var Adult_Leap_2 = 1.55;
                        var Child_Cash_16_2 = 1.30;
                        var Child_Leap_19_2 = 1.00;
                    }
                    else if (commonroutes[i].stage2.number_stops > 3 && commonroutes[i].stage2.number_stops <= 13) {
                        var Adult_Cash_2 = 2.25;
                        var Adult_Leap_2 = 2.00;
                        var Child_Cash_16_2 = 1.30;
                        var Child_Leap_19_2 = 1.00;
                    }
                    else {
                        var Adult_Cash_2 = 3.30;
                        var Adult_Leap_2 = 2.50;
                        var Child_Cash_16_2 = 1.30;
                        var Child_Leap_19_2 = 1.00;
                    }

                    var Adult_Cash_Together = (Adult_Cash_1 + Adult_Cash_2).toFixed(2);
                    var Adult_Leap_Together = (Adult_Leap_1 + Adult_Leap_2).toFixed(2);
                    var Child_Cash_16_Together = (Child_Cash_16_1 + Child_Cash_16_2).toFixed(2);
                    var Child_Leap_19_Together = (Child_Leap_19_1 + Child_Leap_19_2).toFixed(2);

                  
                  
                    window.showMoney2 = function() {
                        var fareLi = $("#showFare").find("p");
                        fareLi.eq(0).html("\&nbsp\&nbspAdult (Cash): €" + Adult_Cash_Together);
                        fareLi.eq(1).html("\&nbsp\&nbspAdult (Leap Card): €" + Adult_Leap_Together);
                        fareLi.eq(2).html("\&nbsp\&nbspChild Under 16 (Cash): €" + Child_Cash_16_Together);
                        fareLi.eq(3).html("\&nbsp\&nbspChild Under 19 (Leap Card): €" + Child_Leap_19_Together);
                        $('tr').removeClass('routeOptions'); 
                    }
                  

                    if (timeToGo != 'Later') {
                        
                     if (Math.round((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) == 0)  {
                   informationTable += "<tbody><tr class='routeOptions'><td style = 'width: 20%'>" + "Due" + "</td><td style = 'width: 20%'>" + Math.round(((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) + commonroutes[i].total_time)  + " mins" + "</td><td style = 'width: 40%'>" + commonroutes[i].stage1.route_short_name + " → " + commonroutes[i].stage2.route_short_name + "</td><td style = 'width: 20%; color:#5af542'><a style='cursor:hand' onclick=\"getFare(); showMoney2()\">Show</a></td><td style='display: none'>NowMultiple</td><td style='display: none'>" + commonroutes[i].changeover_stop_id_short + "</td><td style='display: none'>" + commonroutes[i].stage1.number_stops + "</td><td style='display: none'>" + commonroutes[i].stage2.number_stops + "</td><td style='display: none'>" + commonroutes[i].wait_time + " mins</td></tr></tbody>";  
                         
                     }  
                        
                     else {   
                    informationTable += "<tbody><tr class='routeOptions'><td style = 'width: 20%'>" + Math.round((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) + " mins" + "</td><td style = 'width: 20%'>" + Math.round(((commonroutes[i].start_stop_predicted_arrival_timestamp - mytime)/1000/60) + commonroutes[i].total_time)  + " mins" + "</td><td style = 'width: 40%'>" + commonroutes[i].stage1.route_short_name + " → " + commonroutes[i].stage2.route_short_name + "</td><td style = 'width: 20%; color:#5af542'><a style='cursor:hand' onclick=\"getFare(); showMoney2()\">Show</a></td><td style='display: none'>NowMultiple</td><td style='display: none'>" + commonroutes[i].changeover_stop_id_short + "</td><td style='display: none'>" + commonroutes[i].stage1.number_stops + "</td><td style='display: none'>" + commonroutes[i].stage2.number_stops + "</td><td style='display: none'>" + commonroutes[i].wait_time + " mins</td></tr></tbody>";
                     }
                        
                    }
                    
                    
                    else {
                    informationTable += "<tbody><tr class='routeOptions'><td style = 'width: 20%'>" + getLocalTime(commonroutes[i].start_stop_predicted_arrival_timestamp) + "</td><td style = 'width: 20%'>" + Math.round(commonroutes[i].total_time)  + " mins" + "</td><td style = 'width: 40%'>" + commonroutes[i].stage1.route_short_name + " → " + commonroutes[i].stage2.route_short_name + "</td><td style = 'width: 20%; color:#5af542'><a style='cursor:hand' onclick=\"getFare(); showMoney2()\">Show</a></td><td style='display: none'>LaterMultiple</td><td style='display: none'>" + commonroutes[i].changeover_stop_id_short + "</td><td style='display: none'>" + commonroutes[i].stage1.number_stops + "</td><td style='display: none'>" + commonroutes[i].stage2.number_stops + "</td><td style='display: none'>" + commonroutes[i].wait_time + " mins</td></tr></tbody>";
                    }
                  

                      $(".details").on("click",".routeOptions",function(e){
                             var tdMapShow = $(this).find("td");   
                             var busSeleted = tdMapShow.eq(2).text();
                             var combinationRoute = commonroutes[i].stage1.route_short_name + " → " + commonroutes[i].stage2.route_short_name;
                          

                            if (busSeleted == combinationRoute) {
                            for (var p = 0; p < markersset1.length; p++) {
                                markersset1[p].setMap(null);
                            }
                            for (var p = 0; p < markersset2.length; p++) {
                                markersset2[p].setMap(null);
                            }
                            markersset1 = [];
                            markersset2 = [];

                            if (BusPath1 && BusPath1.setMap) {
                                BusPath1.setMap(null);
                            }
                            if (BusPath2 && BusPath2.setMap) {
                                BusPath2.setMap(null);
                            }
                            pathArray1 = [];
                            pathArray2 = [];

                            for (var j = 0; j < commonroutes[i].stage1.stage_subroute_stops.length; j++) {
                            var get_all_stops_list_1 = commonroutes[i].stage1.stage_subroute_stops[j];
                            var routeLat_1 = get_all_stops_list_1.stop_lat;
                            var routeLng_1 = get_all_stops_list_1.stop_lng;
                            var myLatlng_1 = {
                                lat: routeLat_1,
                                lng: routeLng_1
                            };

                            var marker1 = new google.maps.Marker({
                                position: myLatlng_1,
                                map: map,
                                icon: "https://img.icons8.com/ios-glyphs/30/000000/map-pin.png",
                            });

                            markersset1.push(marker1);

                            (function(marker1,get_all_stops_list_1) {
                                google.maps.event.addListener(marker1, "click", function(e) {
                                    infoWindow.setContent("<div style = 'width: 200px; min-height: 40px; font-style: italic; font-weight: 800'>" + "Stop ID: " + get_all_stops_list_1.stop_id_short + "<br>" + "Address: " + get_all_stops_list_1.stop_name + "<br>" + "Sequence Number: " + get_all_stops_list_1.stop_sequence + "</div>");
                                    infoWindow.open(map, marker1);
                                });
                            })(marker1,get_all_stops_list_1);
                            latlngbounds.extend(marker1.position);
                                
                         var bounds = new google.maps.LatLngBounds();
                         map.setCenter(latlngbounds.getCenter());
                         map.fitBounds(latlngbounds);

                            }//end of for loop
                  
                                         
                    for (var k = 0; k < commonroutes[i].stage1.stage1_subroute_shape_points.length; k++) {
                        var shapeLat_1 = commonroutes[i].stage1.stage1_subroute_shape_points[k].shape_point_lat;
                        var shapeLng_1 = commonroutes[i].stage1.stage1_subroute_shape_points[k].shape_point_lng;
                        var shapeLatLng_1 = {
                            lat: shapeLat_1,
                            lng: shapeLng_1
                        };
                        pathArray1[k] = shapeLatLng_1;
                    }
                            
                    //Draw polylines between bus stops based on their order
                    BusPath1 = new google.maps.Polyline({
                        path: pathArray1,
                        geodesic: true,
                        strokeColor: '#D95C00',
                        strokeOpacity: 1.0,
                        strokeWeight: 4
                    });
                        BusPath1.setMap(map);   
                                
                                

                           for (var j = 0; j < commonroutes[i].stage2.stage_subroute_stops.length; j++) {
                            var get_all_stops_list_2 = commonroutes[i].stage2.stage_subroute_stops[j];
                            var routeLat_2 = get_all_stops_list_2.stop_lat;
                            var routeLng_2 = get_all_stops_list_2.stop_lng;
                            var myLatlng_2 = {
                                lat: routeLat_2,
                                lng: routeLng_2
                            };

                            var marker2 = new google.maps.Marker({
                                position: myLatlng_2,
                                map: map,
                                icon: "https://img.icons8.com/ios-glyphs/30/000000/map-pin.png",
                            });

                            markersset2.push(marker2);

                            (function(marker2,get_all_stops_list_2) {
                                google.maps.event.addListener(marker2, "click", function(e) {
                                    infoWindow.setContent("<div style = 'width: 200px; min-height: 40px; font-style: italic; font-weight: 800'>" + "Stop ID: " + get_all_stops_list_2.stop_id_short + "<br>" + "Address: " + get_all_stops_list_2.stop_name + "<br>" + "Sequence Number: " + get_all_stops_list_2.stop_sequence + "</div>");
                                    infoWindow.open(map, marker2);
                                });
                            })(marker2,get_all_stops_list_2);
                            latlngbounds.extend(marker2.position);
                           }
                                
                        var bounds = new google.maps.LatLngBounds();
                         map.setCenter(latlngbounds.getCenter());
                         map.fitBounds(latlngbounds);
                                
                                
                      for (var k = 0; k < commonroutes[i].stage2.stage2_subroute_shape_points.length; k++) {
                        var shapeLat_2 = commonroutes[i].stage2.stage2_subroute_shape_points[k].shape_point_lat;
                        var shapeLng_2 = commonroutes[i].stage2.stage2_subroute_shape_points[k].shape_point_lng;
                        var shapeLatLng_2 = {
                            lat: shapeLat_2,
                            lng: shapeLng_2
                        };
                        pathArray2[k] = shapeLatLng_2;
                    }
                            
                    //Draw polylines between bus stops based on their order
                    BusPath2 = new google.maps.Polyline({
                        path: pathArray2,
                        geodesic: true,
                        strokeColor: '#6F02BA',
                        strokeOpacity: 1.0,
                        strokeWeight: 4
                    });
                        BusPath2.setMap(map);       
                            }//end of if loop
                      }) //end of function                        
    } //endif loop with transfer
} //outside endfor loop
                                                         
    informationTable += "</table>";
    $(".details").html(informationTable);

                        
   
     //Sort the table retunred by Ajax 
      var table, rows, switching, i, x, y, shouldSwitch;
      table = document.getElementById("myTable");
      switching = true;
      while (switching) {
      switching = false;
      rows = table.rows;
      for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;
          x = rows[i].getElementsByTagName("TD")[1];
          y = rows[i + 1].getElementsByTagName("TD")[1];
          if (Number(x.innerHTML.slice(0,-5)) > Number(y.innerHTML.slice(0,-5))) {
            shouldSwitch = true;
            break;
          }
        }
      if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
        }
      }
        },
    
    error: function(){
        $("#noResult").show();
        setTimeout(function() {
        $("#noResult").hide();;
        }, 3000); //Set the div disappeared after 3 seconds
    }
    });
})