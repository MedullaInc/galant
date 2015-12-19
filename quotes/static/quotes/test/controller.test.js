describe('qtQuoteListController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'http://foo.com/';
 
    beforeEach(function () {
        angular.module('quotes.services.qtServices', []);
        module('quotes.services.qtServices', function ($provide) {
            $provide.factory('Quote', function ($q) {
                var Quote = jasmine.createSpyObj('Quote', ['query', 'fields']);
 
                Quote.query.and.returnValue({$promise: $q.when([{id: 0, last_modified: null}])});
                Quote.fields.and.returnValue({$promise: $q.when({})});
 
                return Quote;
            });
            $provide.factory('QuoteTemplate', function ($q) {
                var QuoteTemplate = jasmine.createSpyObj('QuoteTemplate', ['query', 'fields']);
 
                QuoteTemplate.query.and.returnValue({$promise: $q.when([{id: 0, last_modified: null}])});
                QuoteTemplate.fields.and.returnValue({$promise: $q.when({})});
 
                return QuoteTemplate;
            });
            $provide.factory('Client', function ($q) {
                var Client = jasmine.createSpyObj('Client', ['query', 'fields']);
 
                Client.query.and.returnValue({$promise: $q.when([{id: 0}])});
 
                return Client;
            });
            $provide.factory('Service', function ($q) {
                var Service = jasmine.createSpyObj('Service', ['query', 'fields']);
 
                Service.fields.and.returnValue({$promise: $q.when({})});
 
                return Service;
            });
        });
        module('quotes.controllers.qtQuoteListController', function ($provide) {
        	$provide.value('$uibModal', {open: function () {}});
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
        $controller('qtQuoteListController', {$scope: $scope});
        $scope.init(url);
        $rootScope.$apply();
        $scope.quotes = $scope.quotesSafe;
    });
 
    it('sets quoteDetailURL', function () {
        expect($scope.quoteDetailURL).toEqual(url);
    });
 
    it('generates quoteDetail redirect URL', function () {
        $scope.redirect(4);
        expect($window.location.href).toEqual(url + '4');
    });
 
    it('gets quote list', function () {
        expect($scope.quote.length).toEqual(1);
    });
 
});