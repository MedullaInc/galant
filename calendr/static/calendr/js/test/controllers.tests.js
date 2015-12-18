describe('CalendrControl', function () {
    var $rootScope;
    var $controller;
    var controller;
    var $window;
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
            $provide.value('uiCalendarConfig', {});
            $provide.value('$uibModal', {});
            $provide.value('$aside', {});
            $provide.value('FC', {views: {}});
        });

        inject(function (_$rootScope_, _$controller_, _$window_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $window = _$window_;
        });
    });


    beforeEach(function () {
        var FC = {views: []};
        $scope = $rootScope.$new();
        controller = $controller('clCalendrController', {$scope: $scope});
        $scope.$apply();
    });

    it('loads', function () {
        expect($scope).not.toBeNull();
    });
});
