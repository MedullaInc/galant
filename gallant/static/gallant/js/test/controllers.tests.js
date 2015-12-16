describe('glClientListController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var ClientMock;
    var url = 'http://foo.com/';

    beforeEach(function () {
        module('mocks');
        angular.module('gallant.services.glServices', []);
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('Client', function () {
                return ClientMock;
            });
        });
        module('gallant.controllers.glClientListController', function ($provide) {
            $provide.value('$window', {location: {href: null}});
        });

        inject(function (_ClientMock_) {
            ClientMock = _ClientMock_;
        });

        inject(function (_$rootScope_, _$controller_, _$window_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $window = _$window_;
        });
    });

    var $scope;

    beforeEach(function () {
        $scope = $rootScope.$new();
        $controller('glClientListController', {$scope: $scope});
        $scope.init(url);
        $rootScope.$apply();
        $scope.clients = $scope.clientsSafe;
    });

    it('sets clientDetailURL', function () {
        expect($scope.clientDetailURL).toEqual(url);
    });

    it('generates clientDetail redirect URL', function () {
        $scope.redirect(4);
        expect($window.location.href).toEqual(url + '4');
    });

    it('gets client list', function () {
        expect($scope.clients.length).toEqual(1);
    });

    it('updates client last_modified', function () {
        expect($scope.clients[0].last_contacted).toBeNull();
        $scope.updateLastContacted(0);
        $rootScope.$apply();
        expect($scope.clients[0].last_contacted).not.toBeNull();
    });
});

describe('glFormController', function () {
    var $rootScope;
    var $controller;

    beforeEach(function () {
        module('gallant.controllers.glFormController');

        inject(function (_$rootScope_, _$controller_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
        });
    });

    var $scope;
    var lang = 'es';

    beforeEach(function () {
        $scope = $rootScope.$new();
        $controller('glFormController', {$scope: $scope});
        $scope.init(lang, 'csrftoken');
        $rootScope.$apply();
        $scope.object = {};
    });

    it('sets currentLanguage', function () {
        expect($scope.currentLanguage).toEqual(lang);
    });
});
