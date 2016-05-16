app = angular.module('calendr.controllers.clCalendrController', ['gallant.services.glServices',
    'kanban.directives.kbBoardColumn', 'ui.calendar',
    'ng.django.forms', 'gallant.directives.glMultiDropdown',
]);

app.controller('clCalendrController', function ($window, $scope, Project, User, Task, $compile, $sce,
                                                $timeout, uiCalendarConfig, $filter, FC, moment, glAlertService, clConstants) {
    $scope.clConstants = clConstants;
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $scope.init = function (currentUserId, userResources) {
        $scope.currentUserId = currentUserId
        $scope.userResources = userResources;

        Project.query().$promise.then(function (response) {
            $scope.projects = response;
            if (!userResources) {
                angular.forEach(response, function (p) {
                    $scope.eventResources.push({
                        id: p.id,
                        title: p.name,
                        link: p.link,
                    });
                });

                $scope.$watchCollection('projects', function (newValue, oldValue) {
                    if (oldValue && oldValue.length < newValue.length) {
                        p = newValue[newValue.length - 1];
                        $scope.eventResources.push({
                            id: p.id,
                            title: p.name,
                            link: p.link,
                        });
                    }
                });
            }
        });

        User.query().$promise.then(function (response) {
            $scope.users = response;
            if (userResources) {
                angular.forEach(response, function (u) {
                    $scope.eventResources.push({
                        id: u.id,
                        title: u.email,
                        link: '',
                    });
                });
            }
        });


        /* config object */
        $scope.uiConfig = {
            calendar: {
                schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
                ignoreTimezone: false,
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
                updateEvent: $scope.updateTask,
                dayClick: $scope.dayClick,
                eventDrop: $scope.updateTask,
                eventResize: $scope.updateTask,
                gotoDate: $scope.gotoDate,
                slotWidth: 70,
                resourceLabelText: $scope.userResources ? 'Resources' : 'Projects',
                resourceRender: $scope.projectLink,
            }
        };

        $scope.eventSources = [$scope.tasks];
    };

    FC.views.timelineThreeMonths = {
        type: 'timeline',
        duration: {
            months: 3
        }
    };

    /* event source that contains custom events on the scope */
    $scope.tasks = [];
    $scope.projects = [];
    $scope.eventSources = [];
    $scope.eventResources = [];

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

    var convertToFCFormat = function (task) {
        var ret = angular.copy(task);
        ret.title = ret.name;
        ret.resourceId = $scope.userResources ? ret.assignee : ret.project;
        ret.allDay = false;
        if (!ret.start) {
            // fullcalendar requires start, so add epoch sentinel value
            ret.start = moment(new Date(0));
            ret.end = ret.start;
        } else {
            ret.start = moment(ret.start);
            ret.end = moment(ret.end);
        }
        return ret;
    };

    var convertFromFCFormat = function (task) {
        var ret = angular.copy(task);
        ret.name = ret.title;
        if ($scope.userResources)
            ret.assignee = ret.resourceId;
        else
            ret.project = ret.resourceId;
        delete ret.source;
        try {
            if (!ret.start._d.getTime()) {
                // check for epoch sentinel value (start required by FC), set time to null if present
                ret.start = null;
                ret.end = null;
            }
        } catch (ex) {}
        return ret;
    };

    $scope.editFCTask = function (task) {
        $scope.editTask(convertFromFCFormat(task));
    };

    /* Retrieve all Tasks from API service and add wrapper to calendar event */
    Task.query().$promise.then(function (response) {
        angular.forEach(response, function (task) {
            $scope.tasks.push(convertToFCFormat(task));
        });
        $scope.tasksLoaded = true;
    });

    $scope.updateTask = function (task) {
        Task.update({id: task.id}, convertFromFCFormat(task)).$promise.then(function (response) {
            var idx = $scope.tasks.findIndex(function (t) {
                return t.id == task.id
            });
            if (~idx)
                $scope.tasks[idx] = convertToFCFormat(response);
            glAlertService.add('success', 'Task ' + task.name + ' updated.');
        }, function (error) {
            glAlertService.add('danger', error.data);
        });
    };

    $scope.taskSaved = function (task) {
        var idx = $scope.tasks.findIndex(function (t) { return t.id == task.id; });
        if (~idx)
            $scope.tasks[idx] = convertToFCFormat(task);
        else
            $scope.tasks.push(convertToFCFormat(task));

        $scope.modalInstance.dismiss('cancel');
    };

    $scope.taskDeleted = function (event) {
        if ($window.confirm('Are you sure you want to permanently delete this task?')) {
            Task.delete({id: event.id}).$promise.then(function (response) {
                var index = $scope.tasks.indexOf(response);
                $scope.tasks.splice(index, 1);
                $scope.modalInstance.dismiss('cancel');
            });
        }

    };

    /* alert on eventClick */
    $scope.alertOnEventClick = function (task, jsEvent, view) {
        $scope.editTask(convertFromFCFormat(task));
    };

    /* remove event from calendar */
    $scope.remove = function (index) {
        glAlertService.add('success', 'Task "' + $scope.tasks[index].title + '" has been removed.');
        $scope.tasks.splice(index, 1);
    };

    /* Change View */
    $scope.changeView = function (view, calendar) {
        uiCalendarConfig.calendars[calendar].fullCalendar('changeView', view);
    };

    /* Change View */
    $scope.renderCalendar = function (calendar) {
        if (uiCalendarConfig.calendars[calendar]) {
            uiCalendarConfig.calendars[calendar].fullCalendar('render');
        }
    };

    $scope.selectFunction = function (start, end, x, y, resource) {
        var task = {
            name: '',
            daily_estimate: 0,
            resourceId: +resource.id,
            assignee: $scope.currentUserId,
            start: start,
            end: end
        };

        $scope.editTask(convertFromFCFormat(task));
        uiCalendarConfig.calendars.myCalendar1.fullCalendar('unselect');
    };

    $scope.projectLink = function (resource, labelTd) {
        if (!$scope.userResources)
            labelTd.find('.fc-cell-text').html('<a href="' + resource.link + '">' + resource.title.encodeHtml() + '</a>');
    };
});
