app = angular.module('calendr.controllers.clCalendrController', ['ui.calendar', 'ui.bootstrap', 'ng.django.forms', 'ngAside']);

app.controller('clCalendrController', function ($scope, Project, User, Task, $compile,
                                           $timeout, uiCalendarConfig, $uibModal, $filter, $aside, FC) {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    FC.views.timelineThreeMonths = {
        type: 'timeline',
        duration: {
            months: 3
        }
    }

    /* event source that contains custom events on the scope */
    $scope.events = [];
    $scope.projects = [];
    $scope.eventResources = [];

    $scope.openAsideModal = function () {
        if ($scope.asideInstance) {
            $scope.asideInstance.close();
            delete $scope.asideInstance;
        } else {

            /* istanbul ignore next */
            $scope.asideInstance = $aside.open({
                templateUrl: '/static/calendr/html/aside.html',
                backdrop: false,
                controller: function ($scope, $modalInstance, userEvents, openEditModal) {
                    $scope.events = userEvents;
                    $scope.openEditModal = openEditModal;
                    $scope.ok = function (e) {
                        $modalInstance.close();
                        e.stopPropagation();
                    };
                    $scope.cancel = function (e) {
                        $modalInstance.dismiss();
                        e.stopPropagation();
                    };
                },
                placement: 'right',
                size: 'sm',
                resolve: {
                    userEvents: function () {
                        // Return current user tasks
                        return $filter('filter')($scope.events, {
                            resourceId: currentUserId
                        });
                    },
                    openEditModal: function () {
                        // Return current user tasks
                        return $scope.openEditModal;
                    },
                }
            });
        }

    };

    $scope.gotoDate = function (date) {
        uiCalendarConfig.calendars.myCalendar1.fullCalendar('gotoDate', date);
    };

    $scope.today = function () {
        $scope.dt = new Date();
        $scope.gotoDate($scope.dt);
    };

    // $scope.today();


    // Disable weekend selection
    $scope.disabled = function (date, mode) {
        return (mode === 'day' && (date.getDay() === 0 || date.getDay() === 6));
    };

    $scope.toggleMin = function () {
        $scope.minDate = $scope.minDate ? null : new Date();
    };
    $scope.toggleMin();
    $scope.maxDate = new Date(2020, 5, 22);

    $scope.open = function ($event) {
        $scope.status.opened = true;
    };

    $scope.setDate = function (year, month, day) {
        $scope.dt = new Date(year, month, day);
    };

    $scope.dateOptions = {
        formatYear: 'yy',
        startingDay: 1
    };

    $scope.status = {
        opened: false
    };

    /* Retrieve users from API service */
    $scope.getResources = function (project) {
        options = {};
        if (project) {
            options = {
                project_id: project.id
            };
        }
        User.query(options).$promise.then(function (response) {
            angular.forEach(response, function (value, key) {
                $scope.eventResources.push({
                    id: value.id,
                    title: value.email
                });
            });
        });
    };

    /* Retrieve all Tasks from API service */
    $scope.getTasks = function () {
        Task.query().$promise.then(function (response) {
            angular.forEach(response, function (value, key) {
                $scope.renderEvent(value);
            });

        });
    };

    /* Retrieve all Tasks from API service */
    $scope.getProjects = function () {
        Project.query().$promise.then(function (response) {
            $scope.projects = response;
        });
    };

    $scope.getResources();
    $scope.getProjects();
    $scope.getTasks();


    /* Open edit Modal */
    /* istanbul ignore next */
    $scope.openEditModal = function (event) {
        $scope.event = event;
        $uibModal.open({
            templateUrl: taskModalUrl,
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope, $modalInstance, $log, event, events, resources, projects, updateEvent, createTask) {
                $scope.event = event;
                $scope.events = events;
                $scope.resources = resources;
                $scope.projects = projects;
                $scope.updateEvent = updateEvent;
                $scope.createTask = createTask;

                $scope.submit = function (e) {
                    $modalInstance.dismiss('cancel');
                    // var found = $filter('filter')($scope.events, {id: $scope.event.id}, true)
                    if (e.id) {
                        $scope.updateEvent($scope.event);
                    } else {

                        var task = {
                            "id": "",
                            "user": currentUserId,
                            "name": e.title,
                            "start": e.start,
                            "end": e.end,
                            "daily_estimate": e.daily_estimate,
                            "project": e.projectId,
                            "services": [],
                            "assignee": String(e.resourceId),
                            "notes": []
                        };

                        $scope.createTask(task);
                    }
                };
                $scope.cancel = function () {
                    $modalInstance.dismiss('cancel');
                };
                $scope.deleteTask = function (event) {
                    if (confirm('Are you sure you want to permanently delete this task?')) {
                        Task.delete({id: event.id}).$promise.then(function (response) {
                            var index = $scope.events.indexOf(event);
                            $scope.events.splice(index, 1);
                            $modalInstance.dismiss('cancel');
                        });
                    }

                };
            },
            resolve: {
                event: function () {
                    return $scope.event;
                },
                events: function () {
                    return $scope.events;
                },
                projects: function () {
                    return $scope.projects;
                },
                updateEvent: function () {
                    return $scope.updateEvent;
                },
                createTask: function () {
                    return $scope.createTask;
                },
                resources: function () {
                    return $scope.eventResources;
                },
            }
        });
    };

    /* event triggered on project change */
    $scope.projectChanged = function (project_id) {
        var proj = {
            id: project_id
        };

        // Remove existing resources in calendar.
        $scope.eventResources.splice(0, $scope.eventResources.length);

        // Fetch selected project resources
        $scope.getResources(proj);
    };

    /* update on Calendar */
    $scope.updateEvent = function (event, element) {
        var task = {
            "id": event.id,
            "user": event.user,
            "name": event.title,
            "start": moment(event.start).format(),
            "end": moment(event.end).format(),
            "daily_estimate": event.daily_estimate,
            "project": event.projectId,
            "services": [],
            "assignee": String(event.resourceId),
            "notes": []
        };


        $scope.updateTask(task);
        $scope.alertMessage = ('Task "' + event.title + '" has been relocated.');

        //alert(event.title);
    };

    /* alert on eventClick */
    $scope.alertOnEventClick = function (event, jsEvent, view) {
        //$scope.alertMessage = (event.title + ' was clicked ');
        $scope.openEditModal(event, $scope.eventResources);
        //alert($scope.alertMessage);
    };

    /* alert on Drop */
    $scope.alertOnDrop = function (event, delta, revertFunc, jsEvent, ui, view) {
        $scope.alertMessage = ('Event Dropped to make dayDelta ' + delta);
    };

    /* alert on Resize */
    $scope.alertOnResize = function (event, delta, revertFunc, jsEvent, ui, view) {
        var task = {
            "id": event.id,
            "user": event.user,
            "name": event.title,
            "start": event.start,
            "end": event.end,
            "daily_estimate": event.daily_estimate,
            "project": event.projectId,
            "services": [],
            "assignee": String(event.resourceId),
            "notes": []
        };

        $scope.updateTask(task);
        $scope.alertMessage = ('Task "' + event.title + '" has been resized.');
    };

    /* add custom event*/
    $scope.renderEvent = function (e) {
        var event = {
            id: e.id,
            user: e.user,
            title: e.name || 'n/a',
            start: e.start,
            end: e.end,
            resourceId: String(e.assignee),
            projectId: e.project,
            allDay: false,
            daily_estimate: parseFloat(e.daily_estimate),
        };

        $scope.events.push(event);
        // $scope.eventRender(event);

    };

    /* Event fired on day click */
    /* Deprecated use select instead */
    // $scope.dayClick = function(date, jsEvent, view, resource) {
    //   var task = {
    //     "start": date,
    //     "end": moment(date).add(2, 'hours'),
    //     "assignee": String(resource.id),
    //     "project": 1,
    //   }

    //   // Create new task in calendar
    //   $scope.createTask(task);

    // };


    /* Create a new Task using API Service */
    $scope.createTask = function (task) {
        // Event to task
        var myTask = {
            "id": "",
            "user": currentUserId,
            "name": task.name,
            "start": moment(task.start).format(),
            "end": moment(task.end).format(),
            "daily_estimate": task.daily_estimate,
            "project": task.project,
            "services": [],
            "assignee": task.assignee,
            "notes": []
        };

        $scope.postTask(myTask);
    };

    /* remove event from calendar */
    $scope.remove = function (index) {
        $scope.events.splice(index, 1);
    };

    /* postTask controller Wrapper */
    $scope.postTask = function (task) {
        Task.save(task).$promise.then(function (response) {
            $scope.renderEvent(response);

        });
    };


    /* Update an existing Task using API Service */
    $scope.updateTask = function (task) {


        Task.update(task).$promise.then(function (response) {

            for (i = 0; i < $scope.events.length; i++) {
                if ($scope.events[i].id == response.id) {
                    $scope.events.splice(i, 1);
                }
            }

            $scope.renderEvent(response);
        });

    };

    /* Change View */
    $scope.changeView = function (view, calendar) {

        uiCalendarConfig.calendars[calendar].fullCalendar('changeView', view);

    };

    /* Change View */
    $scope.renderCalender = function (calendar) {
        $timeout(function () {
            if (uiCalendarConfig.calendars[calendar]) {
                uiCalendarConfig.calendars[calendar].fullCalendar('render');
            }
        });
    };

    $scope.eventRender = function (event, element, view) {
    };

    $scope.refetchEvents = function () {
    };

    $scope.selectFunction = function (start, end, x, y, resource) {
        var event;
        event = {
            daily_estimate: 0.0,
            resourceId: resource.id,
            start: start,
            end: end,
            title: "New Task",
        };

        $scope.openEditModal(event);
        uiCalendarConfig.calendars.myCalendar1.fullCalendar('unselect');
    };

    /* config object */
    $scope.uiConfig = {
        calendar: {
            schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
            defaultView: 'timelineMonth',
            header: {
                left: 'title',
                center: '',
                right: 'prev, next'
            },
            height: 'auto',
            editable: true,
            selectable: true,
            select: $scope.selectFunction,
            eventClick: $scope.alertOnEventClick,
            updateEvent: $scope.updateEvent,
            dayClick: $scope.dayClick,
            eventDrop: $scope.updateEvent,
            eventResize: $scope.alertOnResize,
            eventRender: $scope.eventRender,
            gotoDate: $scope.gotoDate,
        }
    };

    $scope.eventSources = [$scope.events];

});