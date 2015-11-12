
angular.module('gallant.controllers', ['ui.calendar', 'ui.bootstrap', 'ng.django.forms'])

.controller('CalendrControl',
  function($scope, Project, User, Task, $compile, $timeout, uiCalendarConfig, $uibModal, $filter) {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    /* event source that contains custom events on the scope */
    $scope.events = [];
    $scope.projects = [];
    $scope.eventResources = []


    /* Retrieve users from API service */
    $scope.getResources = function(project) {
      options = {};
      if (project) {
        options = {project_id: project.id};
      }
      User.query(options).$promise.then(function(response) {
        angular.forEach(response, function(value, key) {
          $scope.eventResources.push({
            id: value.id,
            title: value.email
          });
        });
      });
    }

    /* Retrieve all Tasks from API service */
    $scope.getTasks = function() {
      Task.query().$promise.then(function(response) {
        angular.forEach(response, function(value, key) {
          $scope.renderEvent(
            value.id,
            value.start,
            value.end,
            value.assignee,
            value.name,
            value.project);
        });
      });
    }

    /* Retrieve all Tasks from API service */
    $scope.getProjects = function() {
      Project.query().$promise.then(function(response) {
        $scope.projects = response;
      });
    }

    $scope.getResources();
    $scope.getProjects();
    $scope.getTasks();


    /* Open edit Modal */
    $scope.open = function(event) {
      $scope.event = event;
      $uibModal.open({
        templateUrl: '/static/calendr/html/calendar_modal.html',
        backdrop: true,
        windowClass: 'modal',
        controller: function($scope, $modalInstance, $log, event, events, resources, projects, updateEvent) {
          $scope.event = event;
          $scope.events = events;
          $scope.resources = resources;
          $scope.projects = projects;
          $scope.updateEvent = updateEvent;
          $scope.filterArr = [99999]

          $scope.submit = function() {
            $modalInstance.dismiss('cancel');
            $scope.updateEvent(event);
          }
          $scope.cancel = function() {
            $modalInstance.dismiss('cancel');
          };
        },
        resolve: {
          event: function() {
            return $scope.event;
          },
          events: function() {
            return $scope.events;
          },
          resources: function() {
            return $scope.eventResources;
          },
          projects: function() {
            return $scope.projects;
          },
          updateEvent: function() {
            return $scope.updateEvent;
          },
        }
      });
    };

    /* event triggered on project change */
    $scope.projectChanged = function(project_id) {
      var proj = {
        id: project_id
      };

      // Remove existing resources in calendar.
      $scope.eventResources.splice(0, $scope.eventResources.length);

      // Fetch selected project resources
      $scope.getResources(proj);
    };

    /* update on Calendar */
    $scope.updateEvent = function(event, element) {
      var task = {
        "id": event.id,
        "user": 1,
        "name": event.title,
        "start": event.start,
        "end": event.end,
        "daily_estimate": "10.0",
        "project": event.projectId,
        "services": [],
        "assignee": String(event.resourceId),
        "notes": []
      }


      $scope.updateTask(task);

      //alert(event.title);
    };

    /* alert on eventClick */
    $scope.alertOnEventClick = function(event, jsEvent, view) {
      //$scope.alertMessage = (event.title + ' was clicked ');
      $scope.open(event, $scope.eventResources);
      //alert($scope.alertMessage);
    };

    /* alert on Drop */
    $scope.alertOnDrop = function(event, delta, revertFunc, jsEvent, ui, view) {
      $scope.alertMessage = ('Event Dropped to make dayDelta ' + delta);
    };

    /* alert on Resize */
    $scope.alertOnResize = function(event, delta, revertFunc, jsEvent, ui, view) {
      var task = {
        "id": event.id,
        "user": 1,
        "name": event.title,
        "start": event.start,
        "end": event.end,
        "daily_estimate": "10.0",
        "project": 1,
        "services": [],
        "assignee": String(event.resourceId),
        "notes": []
      }

      $scope.updateTask(task);
      $scope.alertMessage = ('Event Resized to make dayDelta ' + delta);
    };

    /* add custom event*/
    $scope.renderEvent = function(id, start, end, resource, title, project) {
      var event = {
        id: id,
        title: title || 'n/a',
        start: start,
        end: end,
        resourceId: String(resource),
        projectId: String(project),
        allDay: false
      }

      $scope.events.push(event);
      // $scope.eventRender(event);

    };

    /* Event fired on day click */
    $scope.dayClick = function(date, jsEvent, view, resource) {
      var task = {
        "id": "",
        "user": 1,
        "name": "New Task",
        "start": date,
        "end": moment(date).add(2, 'hours'),
        "daily_estimate": "10.0",
        "project": 1,
        "services": [],
        "assignee": String(resource.id),
        "notes": []
      }

      // Create new task in calendar
      $scope.createTask(task);

    };


    /* remove event from calendar */
    $scope.remove = function(index) {
      $scope.events.splice(index, 1);
    };

    /* postTask controller Wrapper */
    $scope.postTask = function(task) {
      Task.save(task).$promise.then(function(response) {
        $scope.renderEvent(
          response.id,
          response.start,
          response.end,
          response.assignee,
          response.name,
          response.project);

      });
    }

    /* Create a new Task using API Service */
    $scope.createTask = function(task) {
      $scope.postTask(task);
    }

    /* Update an existing Task using API Service */
    $scope.updateTask = function(task) {


      Task.update(task).$promise.then(function(response) {

        for (i = 0; i < $scope.events.length; i++) {
          //console.log($scope.events[i]);
          if ($scope.events[i].id == response.id) {
            $scope.events.splice(i, 1);
          }
        }

        $scope.renderEvent(
          response.id,
          response.start,
          response.end,
          response.assignee,
          response.name,
          response.project);

      });

    }

    /* Change View */
    $scope.changeView = function(view, calendar) {

      uiCalendarConfig.calendars[calendar].fullCalendar('changeView', view);

    };

    /* Change View */
    $scope.renderCalender = function(calendar) {
      $timeout(function() {
        if (uiCalendarConfig.calendars[calendar]) {
          uiCalendarConfig.calendars[calendar].fullCalendar('render');
        }
      });
    };

    $scope.eventRender = function(event, element, view) {

    };

    $scope.refetchEvents = function() {};



    /* config object */
    $scope.uiConfig = {
      calendar: {
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
        height: 450,
        editable: true,
        defaultView: 'timelineDay',
        header: {
          left: 'title',
          center: '',
          right: 'today prev,next'
        },
        eventClick: $scope.alertOnEventClick,
        updateEvent: $scope.updateEvent,
        dayClick: $scope.dayClick,
        eventDrop: $scope.alertOnDrop,
        eventResize: $scope.alertOnResize,
        eventRender: $scope.eventRender,
      }
    };

    $scope.eventSources = [$scope.events];

  });