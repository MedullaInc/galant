describe('qtQuoteListController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'http://foo.com/';
 
    beforeEach(function () {
        angular.module('quotes.services.qtServices', []);
        angular.module('ngAnimate', []);
        module('quotes.services.qtServices', function ($provide) {
            $provide.factory('Quote', function ($q) {
                var Quote = jasmine.createSpyObj('Quote', ['query','queryNC', 'fields']);
 
                Quote.query.and.returnValue({$promise: $q.when([{id: 0, last_modified: null}])});
                Quote.queryNC.and.returnValue({$promise: $q.when([{id: 0, last_modified: null}])});
                Quote.fields.and.returnValue({$promise: $q.when({status: ['bla','bla']})});
 
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
        angular.module('ngAnimate', []);
        $controller('qtQuoteListController', {$scope: $scope});
        $scope.init(url, url);
        $rootScope.$apply();
        $scope.quotes = $scope.quotes;
        $scope.quote = $scope.quotes[0];
    });
 
    it('sets quoteDetailURL', function () {
        expect($scope.quoteDetailURL).toEqual(url);
    });
 
    it('generates quoteDetail redirect URL', function () {
        $scope.redirect(4);
        expect($window.location.href).toEqual(url + '4');
    });

    it('gets quote list', function () {
        expect($scope.quotesSafe.length).toEqual(1);
    });

    it('gets quote status list', function () {
        expect($scope.quoteStatus.length).toEqual(2);
    });
 
});


describe('qtPopoverController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'http://foo.com/';
 
    beforeEach(function () {
        angular.module('quotes.services.qtServices', []);
        angular.module('ngAnimate', []);
        module('quotes.services.qtServices', function ($provide) {
            $provide.factory('Quote', function ($q) {
                var Quote = jasmine.createSpyObj('Quote', ['query', 'fields']);
 
                Quote.query.and.returnValue({$promise: $q.when([{id: 1}])});
                Quote.fields.and.returnValue({$promise: $q.when({})});
 
                return Quote;
            });
            $provide.factory('QuoteTemplate', function ($q) {
                var QuoteTemplate = jasmine.createSpyObj('QuoteTemplate', ['query', 'fields']);
 
                QuoteTemplate.query.and.returnValue({$promise: $q.when([{id: 1}])});
                QuoteTemplate.fields.and.returnValue({$promise: $q.when({})});
 
                return QuoteTemplate;
            });
        });
        module('quotes.controllers.qtPopoverController', function ($provide) {
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
        $controller('qtPopoverController', {$scope: $scope});
        $scope.init(url, url);
        $rootScope.$apply();
        $scope.quotes = $scope.quotes;
        $scope.quote = $scope.quotes[0];
    });
 
    it('sets addQuoteURL', function () {
        expect($scope.addQuoteURL).toEqual(url);
    });
 
    it('generates addQuoteRedirect redirect URL', function () {
        $scope.addQuoteRedirect();
        expect($window.location.href);
    });

    it('generates redirectTemplate redirect URL', function () {
        $scope.redirectTemplate({id:0, languageSelection: "en"});
        expect($window.location.href);
    });

    it('opens and closes modal', function () {
        expect($scope.modalInstance).not.toBeDefined();
        $scope.modalInstance = $scope.open();
        expect($scope.modalInstance).toBeDefined();
    });

    it('changes language', function () {
        $scope.languageSelection({id: 0}, "en");
    });

 
});