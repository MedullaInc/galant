app = angular.module('calendr.controllers.clCalendrController', [
    'ui.calendar', 'ui.bootstrap', 'ng.django.forms', 'gallant.directives.glMultiDropdown',
]);

app.controller('clCalendrController', function ($scope, Project, User, Task, $compile, $sce,
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
    }

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
        $scope.openEditModal(task);
    };

    /* Open edit Modal */
    /* istanbul ignore next */
    $scope.openEditModal = function (task, date) {
        $scope.task = task;
        $uibModal.open({
            templateUrl: '/static/calendr/html/calendar_modal.html',
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope, $uibModalInstance, $log, task, tasks, users, projects, updateTask, gotoDate, currentUserId) {
                $scope.task = task || {
                        assignee: currentUserId,
                        daily_estimate: 0,
                    };

                // Date pickers
                $scope.openStartDatePicker = function () {
                    $scope.start_date_opened = true;
                };

                $scope.openEndDatePicker = function () {
                    $scope.end_date_opened = true;
                };

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
                $scope.users = users;
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
                            var idx = $scope.tasks.findIndex(function (t) {
                                return t.id == task.id
                            });
                            if (~idx)
                                $scope.tasks[idx] = convertToFCFormat(response);
                            glAlertService.add('success', 'Task ' + task.name + ' updated.');
                        }, function (error) {
                            glAlertService.add('danger', error.data);
                        });
                    } else {
                        Task.save(task).$promise.then(function (response) {
                            $scope.tasks.push(convertToFCFormat(response));
                            glAlertService.add('success', 'Task ' + task.name + ' created.');
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
                users: function () {
                    return $scope.users;
                },
                currentUserId: function () {
                    return $scope.currentUserId;
                },
            }
        });
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
        $scope.openEditModal(convertFromFCFormat(task), $scope.projects);
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

        $scope.openEditModal(convertFromFCFormat(task));
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
