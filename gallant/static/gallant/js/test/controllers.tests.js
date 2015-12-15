describe('glClientListController', function () {
    var $rootScope;
    var $controller;
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
        module('gallant.controllers.glClientListController');

        inject(function (_ClientMock_) {
            ClientMock = _ClientMock_;
        });

        inject(function (_$rootScope_, _$controller_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
        });
    });

    describe('$scope.init', function () {
        it('sets clientDetailURL', function () {
            var $scope = $rootScope.$new();
            var controller = $controller('glClientListController', {$scope: $scope});
            $scope.init(url);
            expect($scope.clientDetailURL).toEqual(url);
        });
    });
});
