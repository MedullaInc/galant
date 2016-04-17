app = angular.module('calendr.controllers.clCalendrController', [
    'ui.calendar', 'ui.bootstrap', 'ng.django.forms', 'gallant.directives.glMultiDropdown'
]);

app.controller('clCalendrController', function ($scope, Project, User, Task, $compile,
                                                $timeout, uiCalendarConfig, $uibModal, $filter, FC, moment, glAlertService) {
    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    $scope.init = function (currentUserId) {
        $scope.currentUserId = currentUserId
    }

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
    $scope.getResources = function (options) {
        User.query(options).$promise.then(function (response) {
            angular.forEach(response, function (value, key) {
                $scope.eventResources.push({
                    id: value.id,
                    title: value.email
                });
            });
        });
    };

    var wrapTask = function (task) {
        task.title = task.name;
        task.projectId = task.project;
        task.resourceId = task.assignee;
        task.allDay = false;
        return task;
    };

    var unwrapTask = function (task) {
        task.name = task.title;
        task.project = task.projectId;
        task.assignee = task.resourceId;
        delete task.source;
        return task;
    };

    /* Retrieve all Tasks from API service and add wrapper to calendar event */
    Task.query().$promise.then(function (response) {
        angular.forEach(response, function (task) {
            $scope.tasks.push(wrapTask(task));
        });
    });

    $scope.updateTask = function (task) {
        Task.update({id: task.id}, unwrapTask(task)).$promise.then(function (response) {
            glAlertService.add('success', 'Task ' + task.name + 'updated.');
        });
    }

    /* Retrieve all Tasks from API service */
    $scope.getProjects = function () {
        Project.query().$promise.then(function (response) {
            $scope.projects = response;
        });
    };

    $scope.getResources();
    $scope.getProjects();

    /* Open edit Modal */
    /* istanbul ignore next */
    $scope.openEditModalandgotoDate = function (task) {
        $scope.gotoDate(task.start);
        $scope.openEditModal(task);
    };

    /* Open edit Modal */
    /* istanbul ignore next */
    $scope.openEditModal = function (task) {
        $scope.task = task;
        $uibModal.open({
            templateUrl: '/static/calendr/html/calendar_modal.html',
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope, $uibModalInstance, $log, task, tasks, resources, projects, updateTask, gotoDate) {
                $scope.task = task || {};

                // Date pickers
                $scope.openStartDatePicker = function () {
                    $scope.start_date_opened = true;
                };

                $scope.openEndDatePicker = function () {
                    $scope.end_date_opened = true;
                };

                $scope.task = task;

                if ($scope.task.start) {
                    $scope.task.start = new Date($scope.task.start);
                } else {
                    $scope.task.start = new Date();
                }

                if ($scope.task.end) {
                    $scope.task.end = new Date($scope.task.end);
                } else {
                    $scope.task.end = new Date();
                }

                if (!$scope.task.services)
                    $scope.task.services = [];
                $scope.tasks = tasks;
                $scope.resources = resources;
                $scope.projects = projects;
                $scope.updateTask = updateTask;
                $scope.gotoDate = gotoDate;

                $scope.project = $scope.projects.find(function (p) {
                    return p.id == $scope.task.projectId
                });

                if ($scope.project && $scope.project.services.length) {
                    $scope.availableServices = $scope.project.services;
                }

                $scope.submit = function (task) {
                    $uibModalInstance.dismiss('cancel');
                    // var found = $filter('filter')($scope.events, {id: $scope.event.id}, true)
                    if (task.id) {
                        Task.update({id: task.id}, task).$promise.then(function (response) {
                            var idx = $scope.tasks.findIndex(function (t) { return t.id == task.id });
                            if (~idx)
                                $scope.tasks[idx] = wrapTask(response);
                            glAlertService.add('success', 'Task updated.');
                        }, function (error) {
                            glAlertService.add('danger', error.data);
                        });
                    } else {
                        Task.save(task).$promise.then(function (response) {
                            $scope.tasks.push(wrapTask(response));
                            glAlertService.add('success', 'Task created.');
                        }, function (error) {
                            glAlertService.add('danger', error.data);
                        });
                    }
                    $scope.gotoDate(task.start);
                };

                $scope.cancel = function () {
                    $uibModalInstance.dismiss('cancel');
                };

                $scope.deleteTask = function (task) {
                    if (confirm('Are you sure you want to permanently delete this task?')) {
                        Task.delete({id: task.id}).$promise.then(function (response) {
                            var index = $scope.tasks.indexOf(task);
                            $scope.tasks.splice(index, 1);
                            $uibModalInstance.dismiss('cancel');
                        });
                    }

                };

                $scope.projectChanged = function (projectId) {
                    $scope.project = $scope.projects.find(function (p) {
                        return p.id == projectId
                    });
                    if ($scope.project && $scope.project.services)
                        $scope.availableServices = $scope.project.services;
                    else
                        $scope.availableServices = [];
                    $scope.task.services = [];
                };
            },
            resolve: {
                gotoDate: function () {
                    return $scope.gotoDate;
                },
                task: function () {
                    return $scope.task;
                },
                tasks: function () {
                    return $scope.tasks;
                },
                updateTask: function () {
                    return $scope.updateTask;
                },
                projects: function () {
                    return $scope.projects;
                },
                resources: function () {
                    return $scope.eventResources;
                },
            }
        });
    };

    /* event triggered on project change */
    $scope.projectChanged = function (projectId) {
        var options = {};
        if (projectId)
            options.project_id = projectId;

        // Remove existing resources in calendar.
        $scope.eventResources.splice(0, $scope.eventResources.length);

        // Fetch selected project resources
        $scope.getResources(options);
    };

    /* alert on eventClick */
    $scope.alertOnEventClick = function (task, jsEvent, view) {
        $scope.openEditModal(unwrapTask(task), $scope.eventResources);
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
        };

        $scope.openEditModal(unwrapTask(task));
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
            updateEvent: $scope.updateTask,
            dayClick: $scope.dayClick,
            eventDrop: $scope.updateTask,
            eventResize: $scope.updateTask,
            gotoDate: $scope.gotoDate,
        }
    };

    $scope.eventSources = [$scope.tasks];
});
