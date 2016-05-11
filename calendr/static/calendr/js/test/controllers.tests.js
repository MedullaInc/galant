beforeEach(function () {
    currentUserId = 0;
});

describe('CalendrControl', function () {
    var $rootScope;
    var $controller;
    var $injector;
    var $scope;

    beforeEach(function () {
        angular.module('gallant.services.glServices', []);
        module('gallant.services.glServices', function ($provide) {
            var getMockResource = function ($q) {
                var MockResource = {};
                MockResource.update = function (id, t) {
                    return {$promise: $q.when(t)};
                };
                MockResource.query = function () {
                    return {$promise: $q.when([{id: 0}])};
                };
                MockResource.delete = function (a) {
                    return {$promise: $q.when(a)};
                };

                return MockResource;
            };

            $provide.factory('User', getMockResource);
            $provide.factory('Task', getMockResource);
            $provide.factory('Project', getMockResource);

        });
        angular.module('ui.calendar', []);
        angular.module('ui.bootstrap', []);
        angular.module('ng.django.forms', []);
        angular.module('ngAside', []);
        module('calendr.controllers.clCalendrController', function ($provide) {
            $provide.value('uiCalendarConfig', {calendars: {myCalendar1: {fullCalendar: {}}}});
            $provide.value('$uibModal', {
                open: function () {
                }
            });
            $provide.value('FC', {views: {}});
            $provide.value('moment', {});
            $provide.value('clConstants', {});
            $provide.value('glAlertService', {
                add: function (a, b) {
                    return [{type: 'success', msg: 'a'}]
                }
            });

            $provide.factory('$window', function () {
                return {
                    confirm: function (m) {
                        return true;
                    }
                };
            });

        });

        inject(function (_$rootScope_, _$controller_, _$injector_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $injector = _$injector_;
        });
    });


    beforeEach(function () {
        var FC = {views: []};
        $scope = $rootScope.$new();
        $scope.editTask = function () {
        };
        $controller('clCalendrController', {$scope: $scope});
        $scope.$apply();
    });

    it('loads', function () {
        expect($scope).not.toBeNull();
    });

    it('calls fullcalendar via today()', function () {
        var uiCalendarConfig = $injector.get('uiCalendarConfig');
        spyOn(uiCalendarConfig.calendars.myCalendar1, 'fullCalendar');
        $scope.today();
        expect(uiCalendarConfig.calendars.myCalendar1.fullCalendar).toHaveBeenCalled();
    });

    it('disables weekend selection', function () {
        expect($scope.disabled({
            getDay: function () {
                return 0;
            }
        }, 'day')).toBeTruthy();
        expect($scope.disabled({
            getDay: function () {
                return 3;
            }
        }, 'day')).toBeFalsy();
    });

    it('sets open', function () {
        $scope.status = {opened: false};
        $scope.open();
        expect($scope.status.opened).toBeTruthy();
    });

    it('sets date', function () {
        $scope.setDate();
        expect($scope.dt).toBeDefined();
    });

    //it('updates tasks on project change', function () {
    //    $scope.eventResources = [{}, {}];
    //    expect($scope.eventResources.length).toEqual(2);
    //    $scope.projectChanged(0);
    //    $scope.$apply();
    //    expect($scope.eventResources.length).toEqual(1);
    //});

    it('updates event', function () {
        var glAlertService = $injector.get('glAlertService');
        spyOn(glAlertService, 'add').and.callThrough();
        $scope.updateTask({id: 0, title: 'foo'});
        $scope.$apply();
        expect(glAlertService.add).toHaveBeenCalled();
    });

    it('alerts on event click', function () {
        spyOn($scope, 'editTask');
        $scope.alertOnEventClick({id: 0, title: 'bar'});
        $scope.$apply();
        expect($scope.editTask).toHaveBeenCalled();
    });

    it('removes event', function () {
        var glAlertService = $injector.get('glAlertService');
        spyOn(glAlertService, 'add');
        $scope.remove(0);
        $scope.$apply();
        expect(glAlertService.add).toHaveBeenCalled();
    });

    it('selectFunction', function () {
        var uiCalendarConfig = $injector.get('uiCalendarConfig');
        spyOn(uiCalendarConfig.calendars.myCalendar1, 'fullCalendar');
        $scope.selectFunction({
            getTime: function () {
            }
        }, {}, {}, {}, {});
        expect(uiCalendarConfig.calendars.myCalendar1.fullCalendar).toHaveBeenCalled();
    });

    it('changeView', function () {
        var uiCalendarConfig = $injector.get('uiCalendarConfig');
        spyOn(uiCalendarConfig.calendars.myCalendar1, 'fullCalendar');
        $scope.changeView({}, 'myCalendar1');
        expect(uiCalendarConfig.calendars.myCalendar1.fullCalendar).toHaveBeenCalled();
    });

    it('renderCalendar', function () {
        var uiCalendarConfig = $injector.get('uiCalendarConfig');
        spyOn(uiCalendarConfig.calendars.myCalendar1, 'fullCalendar');
        $scope.renderCalendar('myCalendar1');
        expect(uiCalendarConfig.calendars.myCalendar1.fullCalendar).toHaveBeenCalled();
    });

    it('saves task', function () {
        $scope.modalInstance = {
            dismiss: function () {
            }
        };
        $scope.taskSaved({});
        expect($scope.tasks.length).toEqual(1);
    });

    it('deletes task', function () {
        var Task = $injector.get('Task');
        spyOn(Task, 'delete').and.callThrough();
        $scope.taskDeleted({id: 0});
        expect(Task.delete).toHaveBeenCalled();
    });

    it('edit FC task', function () {
        spyOn($scope, 'editTask');
        $scope.editFCTask({});
        expect($scope.editTask).toHaveBeenCalled();
    });

    it('loads projectLink', function () {
        spyOn($scope, 'projectLink').and.callThrough();
        $scope.projectLink({title: {encodeHtml: function(){}}},{find: function() { return {html: function () {}}; } });
        expect($scope.projectLink).toHaveBeenCalled();
    });

});
