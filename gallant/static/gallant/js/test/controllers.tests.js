describe('glClientListController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'http://foo.com/';

    beforeEach(function () {
        angular.module('gallant.services.glServices', []);
        module('gallant.services.glServices', function ($provide) {
            $provide.factory('Client', function ($q) {
                var Client = jasmine.createSpyObj('Client', ['query', 'fields', 'update']);

                Client.query.and.returnValue({$promise: $q.when([{id: 0, last_contacted: null}])});
                Client.fields.and.returnValue({$promise: $q.when({})});
                Client.update.and.returnValue({$promise: $q.when({})});

                return Client;
            });
        });
        module('gallant.controllers.glClientListController', function ($provide) {
            $provide.value('$window', {location: {href: null}});
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
    var window;

    beforeEach(function () {
        module('gallant.controllers.glFormController');

        inject(function (_$rootScope_, _$controller_, _$window_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $controller = _$controller_;
            $window = _$window_;
        });
    });

    var $scope;
    var lang = 'es';
    var url = 'http://foo.com/';

    beforeEach(function () {
        $scope = $rootScope.$new();
        $controller('glFormController', {$scope: $scope});
        $scope.init(lang, 'csrftoken');
        $rootScope.$apply();
        $scope.object = {};

        $scope.objectEndpoint = {};
        $scope.objectEndpoint.save = function (a, b, callback) {
            callback({ redirect: url });
        };
        $scope.objectEndpoint.update = function (a, b, callback) {
            callback({ redirect: url });
        };
        $scope.objectEndpoint.delete = function (a, callback) {
            callback({ redirect: url });
        };

        spyOn($scope.objectEndpoint, 'save').and.callThrough();
        spyOn($scope.objectEndpoint, 'update').and.callThrough();
        spyOn($scope.objectEndpoint, 'delete').and.callThrough();

        $scope.forms = [{
            $invalid: false, field: {
                $dirty: false, $setDirty: function () {
                    this.$dirty = true;
                }
            },
            innerForm: {
                $invalid: false
            }
        }];
    });

    it('sets currentLanguage', function () {
        expect($scope.currentLanguage).toEqual(lang);
    });

    it('sets forms dirty', function () {
        $scope.submitForm();
        expect($scope.forms[0].field.$dirty).toEqual(true);
    });

    it('saves on submit', function () {
        $scope.submitForm();
        expect($scope.objectEndpoint.save).toHaveBeenCalled();
    });

    it('updates on submit', function () {
        $scope.object = {id: 1};
        $scope.submitForm();
        expect($scope.objectEndpoint.update).toHaveBeenCalled();
    });

    it('deletes object', function () {
        $scope.object = {id: 1};
        $scope.deleteObject();
        expect($scope.objectEndpoint.delete).toHaveBeenCalled();
    });

    it('skips when forms invalid', function () {
        $scope.forms[0].$invalid = true;
        $scope.submitForm();
        expect($scope.objectEndpoint.save).not.toHaveBeenCalled();
    });

    it('adds onbeforeunload when object changes', function () {
        $scope.object = {id: 1};
        $rootScope.$apply();
        $scope.object = {id: 2};
        $rootScope.$apply();
        expect($window.onbeforeunload).not.toBeNull();
        expect($window.onbeforeunload().length).not.toEqual(0);
        $window.onbeforeunload = null; // remove so browser doesn't get stuck
    });

    it('adds onload function', function () {
        $rootScope.$apply();
        var result = $window.onload();
        expect(result).not.toBeNull();
        $window.onload = null; // remove so browser doesn't get stuck
    });

});



