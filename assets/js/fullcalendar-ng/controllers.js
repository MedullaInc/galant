//angular.module('gallant.controllers', ['ajoslin.promise-tracker']).

angular.module('gallant.controllers', ['ui.calendar', 'ui.bootstrap','ng.django.forms'])


.controller('CalendrControl',
   function($scope, gallantAPIservice, $compile, $timeout, uiCalendarConfig) {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $scope.changeTo = 'Hungarian';

    /* event source that contains custom events on the scope */
    $scope.events = [

    ];


    $scope.eventResources = []


    /* alert on eventClick */
    $scope.alertOnEventClick = function( date, jsEvent, view){
        $scope.alertMessage = (date.title + ' was clicked ');
        alert($scope.alertMessage);
    };

    /* alert on Drop */
     $scope.alertOnDrop = function(event, delta, revertFunc, jsEvent, ui, view){
       $scope.alertMessage = ('Event Dropped to make dayDelta ' + delta);
    };
    /* alert on Resize */
    $scope.alertOnResize = function(event, delta, revertFunc, jsEvent, ui, view ){
       $scope.alertMessage = ('Event Resized to make dayDelta ' + delta);
    };

    /* add and removes an event source of choice */
    $scope.addRemoveEventSource = function(sources,source) {
      var canAdd = 0;
      angular.forEach(sources,function(value, key){
        if(sources[key] === source){
          sources.splice(key,1);
          canAdd = 1;
        }
      });
      if(canAdd === 0){
        sources.push(source);
      }
    };

    /* add custom event*/
    $scope.renderEvent = function(start,end,resource) {

      var event = {
          title: 'Some Event',
          start: start,
          end: end,
          className: ['openSesame'],
          resourceId: resource,
          allDay: false
      }

      $scope.events.push(event);

    };

    $scope.alertOnDayClick = function(date, jsEvent, view, resource) {
        // $scope.alertMessage = (date + ' was clicked ');
        
        var event = {
        "id": 7,
        "user": 1,
        "name": "Some test",
        "start": date,
        "end": moment(date).add(2, 'hours'),
        "daily_estimate": "10.0",
        "project": 1,
        "services": [],
        "assignee": resource.id,
        "notes": []
        }

        gallantAPIservice.postTask(event).success(function(response) {
        $scope.renderEvent( response.start,
                            response.end,
                            response.assignee
                            );
            
        });

        // $('#add_task').modal('show');
        // var myEvent = {
        //   title:"my new event",
        //   allDay: false,
        //   start: date.format(),
        //   end: date.format(),
        //   resourceId: resource.id
        // };
        // $('#calendar').fullCalendar('renderEvent', myEvent, true);

    };

    /* remove event */
    $scope.remove = function(index) {
      $scope.events.splice(index,1);
    };

    $scope.getResources = function() {
      gallantAPIservice.getUsers().success(function(response) {
        angular.forEach(response, function(value, key) {
          $scope.eventResources.push({id:value.id, title:value.email});
        });
    });
    }
      
    $scope.getTasks = function() {
      gallantAPIservice.getTasks().success(function(response) {

        angular.forEach(response, function(value, key) {
          $scope.renderEvent(value.start,value.end,value.assignee);
        });     
      });
    }

    /* Change View */
    $scope.changeView = function(view,calendar) {
      uiCalendarConfig.calendars[calendar].fullCalendar('changeView',view);
    };

    /* Change View */
    $scope.renderCalender = function(calendar) {
      $scope.getResources();
      $scope.getTasks();

      $timeout(function() {
        if(uiCalendarConfig.calendars[calendar]){
          uiCalendarConfig.calendars[calendar].fullCalendar('render');
        }
      });
    };
    
     /* Render Tooltip */
    $scope.eventRender = function( event, element, view ) {
        // element.attr({'tooltip': event.title,
        //               'tooltip-append-to-body': true});
        // $compile(element)($scope);
    };

    /* config object */
    $scope.uiConfig = {
      calendar:{
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
        height: 450,
        editable: true,
        defaultView: 'timelineDay',
        header:{
          left: 'title',
          center: '',
          right: 'today prev,next'
        },
        eventClick: $scope.alertOnEventClick,
        dayClick: $scope.alertOnDayClick,
        eventDrop: $scope.alertOnDrop,
        eventResize: $scope.alertOnResize,
        eventRender: $scope.eventRender
      }
    };

    $scope.changeLang = function() {
      if($scope.changeTo === 'Hungarian'){
        $scope.uiConfig.calendar.dayNames = ["Vasárnap", "Hétfő", "Kedd", "Szerda", "Csütörtök", "Péntek", "Szombat"];
        $scope.uiConfig.calendar.dayNamesShort = ["Vas", "Hét", "Kedd", "Sze", "Csüt", "Pén", "Szo"];
        $scope.changeTo= 'English';
      } else {
        $scope.uiConfig.calendar.dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
        $scope.uiConfig.calendar.dayNamesShort = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        $scope.changeTo = 'Hungarian';
      }
    };
    /* event sources array*/
    

    $scope.eventSources = [$scope.events];




   
    
   


    
    
});

