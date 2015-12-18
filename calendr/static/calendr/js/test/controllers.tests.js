describe('CalendrControl', function () {
    var $rootScope;
    var $controller;
    var $injector;
    var $scope;

    beforeEach(function () {
        angular.module('gallant.services.glServices', []);
        module('gallant.services.glServices', function ($provide) {
            var getMockResource = function ($q) {
                var MockResource = function () { return {id: 0}; };
                MockResource.get = function () { return {$promise: $q.when({id: 0})}; };
                MockResource.query = function () { return {$promise: $q.when([{id: 0}])}; };
                return MockResource;
            }

            $provide.factory('User', getMockResource);
            $provide.factory('Task', getMockResource);
            $provide.factory('Project', getMockResource);
        });
        angular.module('ui.calendar', []);
        angular.module('ui.bootstrap', []);
        angular.module('ng.django.forms', []);
        angular.module('ngAside', []);
        module('calendr.controllers.clCalendrController', function ($provide) {
            $provide.value('uiCalendarConfig', {calendars:{myCalendar1: {fullCalendar: function (a, b) {}}}});
            $provide.value('$uibModal', {});
            $provide.value('$aside', {open: function () { return {close: function () {}}; }});
            $provide.value('FC', {views: {}});
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
        $controller('clCalendrController', {$scope: $scope});
        $scope.$apply();
    });

    it('loads', function () {
        expect($scope).not.toBeNull();
    });

    it('opens and closes aside', function () {
        expect($scope.asideInstance).not.toBeDefined();
        $scope.openAsideModal();
        expect($scope.asideInstance).toBeDefined();
        $scope.openAsideModal();
        expect($scope.asideInstance).not.toBeDefined();
    });

    it('calls fullcalendar via today()', function () {
        var uiCalendarConfig = $injector.get('uiCalendarConfig');
        spyOn(uiCalendarConfig.calendars.myCalendar1, 'fullCalendar');
        $scope.today();
        expect(uiCalendarConfig.calendars.myCalendar1.fullCalendar).toHaveBeenCalled();
    });

    it('disables weekend selection', function () {
        expect($scope.disabled({getDay: function() { return 0; }}, 'day')).toBeTruthy();
        expect($scope.disabled({getDay: function() { return 3; }}, 'day')).toBeFalsy();
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
});
