describe('qtForm', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('quotes.directives.qtForm');
        module('staticNgTemplates');
        angular.module('ngAnimate', []);
        angular.module('as.sortable', []);
        angular.module('ui.bootstrap', []); 

        angular.module('quotes.services.qtServices', []);
        module('quotes.services.qtServices', function ($provide) { 
            $provide.factory('Quote', function ($q) {
                var Quote = function () { return {id: 0}; };
                Quote.get = function () { return {$promise: $q.when({id: 0})}; };
                Quote.fields = function () { return {$promise: $q.when({status: ['status', 'status'], language: ['language', 'language']})}; };
                return Quote;
            });

            $provide.factory('QuoteTemplate', function ($q) {
                var QuoteTemplate = function () { return {id: 0}; };
                QuoteTemplate.get = function () { return {$promise: $q.when({id: 0})}; };
                return QuoteTemplate;
            });

            $provide.factory('Client', function ($q) {
                var Client = jasmine.createSpyObj('Client', ['get', 'fields']);
                Client.get.and.returnValue({$promise: $q.when([{id: 0}])});
                return Client;
            });

            $provide.factory('Service', function ($q) {
                var Service = jasmine.createSpyObj('Service', ['get', 'fields']);
                Service.get.and.returnValue({$promise: $q.when([{id: 0}])});
                Service.fields.and.returnValue({$promise: $q.when({type: ['type', 'type']})});
                return Service;
            });

        });
        module('quotes.directives.qtForm', function ($provide) {
            $provide.value('$uibModal', {open: function () {}});
            $provide.value('$window', {location: {href: null}});
        });
        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });
 
        $rootScope.language = 'en';
        $rootScope.text = {en: 'sadf'}
        $scope = $rootScope.$new();
    });

  describe('qtQuoteForm', function () {

        beforeEach(function () {
            $scope.quote = {type: 'Quote'};
            $scope.quoteTemplate = {type: 'QuoteTemplate'};
            $scope.language = 'en';
            $scope.endpoint = $scope.quote;
        });

        it('compiles', function () {
            var element = $compile('<div quote-id="0" quote="quote" qt-quote-form language="language"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<div cla');
        });
 
        it('compiles with quote id and bool-template false', function () {
            var element = $compile('<div qt-quote-form quote="quote" quote-id="0" bool-template="False"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<div cla');
        });

        it('compiles with quote id and bool-template true', function () {
            var element = $compile('<div qt-quote-form quote="quote" quote-id="0" bool-template="True"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<div cla');
        });
 
        it('compiles with quote template id and bool-template true', function () {
            var element = $compile('<div qt-quote-form quote="quote" template-id="0" bool-template="True"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<div cla');
        });

        it('adds service', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote" ></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().addService();
            expect($scope.quote.services.length).toEqual(2);
        });
 
        it('remove service', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().removeService();
            expect($scope.quote.services.length).toEqual(0);
        });
 
        it('adds section', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().addSection();
            expect($scope.quote.sections.length).toEqual(3);
        });

        it('remove section', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().removeSection();
            expect($scope.quote.sections.length).toEqual(1);
        });

        it('changes language', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().changeLanguage(["en","en"]);
            expect($scope.language.length).toEqual(2);
        });

    });
});
 
