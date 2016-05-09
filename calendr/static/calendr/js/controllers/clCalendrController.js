app = angular.module('calendr.controllers.clCalendrController', ['gallant.services.glServices',
    'kanban.directives.kbBoardColumn', 'ui.calendar',
    'ng.django.forms', 'gallant.directives.glMultiDropdown',
]);

app.controller('clCalendrController', function ($scope, Project, User, Task, $compile, $sce,
                                                $timeout, uiCalendarConfig, $filter, FC, moment, glAlertService, clConstants) {
    $scope.clConstants = clConstants;
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $scope.init = function (currentUserId) {
        $scope.currentUserId = currentUserId
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

    /* Retrieve users from API service */
    User.query().$promise.then(function (response) {
        $scope.users = response;
    });

    var convertToFCFormat = function (task) {
        task.title = task.name;
        task.resourceId = task.project;
        task.allDay = false;
        return task;
    };

    var convertFromFCFormat = function (task) {
        task.name = task.title;
        task.project = task.resourceId;
        delete task.source;
        return task;
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

    /* Retrieve all Tasks from API service */
    $scope.getProjects = function () {
        Project.query().$promise.then(function (response) {
            $scope.projects = response;
            angular.forEach(response, function (p) {
                $scope.eventResources.push({
                    id: p.id,
                    title: p.name,
                    link: p.link,
                });
            });
        });
    };

    // currently only adding a new project is reflected in FC
    $scope.$watchCollection('projects', function (newValue, oldValue) {
        if (oldValue && oldValue.length < newValue.length) {
            p = newValue[newValue.length-1];
            $scope.eventResources.push({
                id: p.id,
                title: p.name,
                link: p.link,
            });
        }
    });

    // $scope.getResources();
    $scope.getProjects();

    /* Open edit Modal */
    /* istanbul ignore next */
    $scope.openEditModalandgotoDate = function (task) {
        $scope.gotoDate(task.start);
        $scope.editTask(task);
    };

    /* event triggered on project change */
    //$scope.projectChanged = function (projectId) {
    //    var options = {};
    //    if (projectId)
    //        options.project_id = projectId;
    //
    //    // Remove existing resources in calendar.
    //    $scope.eventResources.splice(0, $scope.eventResources.length);
    //
    //    // Fetch selected project resources
    //    $scope.getResources(options);
    //};

    /* alert on eventClick */
    $scope.alertOnEventClick = function (task, jsEvent, view) {
        $scope.editTask(convertFromFCFormat(task));
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
        labelTd.find('.fc-cell-text').html('<a href="' + resource.link + '">' + resource.title.encodeHtml() + '</a>');
    };

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
            resourceLabelText: 'Projects',
            resourceRender: $scope.projectLink,
        }
    };

    $scope.eventSources = [$scope.tasks];
});
