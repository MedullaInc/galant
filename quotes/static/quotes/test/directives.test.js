describe('qtForm', function () {
    var $rootScope;
    var $compile;
    var $scope;
 
    beforeEach(function () {
        module('quotes.directives.qtForm');
        module('staticNgTemplates');
        angular.module('as.sortable', []);
        angular.module('ui.bootstrap', []); 


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
        it('compiles', function () {
            var element = $compile('<div qt-quote-form></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<div cla');
        });
 
        it('compiles with quote id', function () {
            var element = $compile('<div qt-quote-form quote="quote" quote-id="0"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<div cla');
        });
 
        it('compiles with quote template id', function () {
            var element = $compile('<div qt-quote-form quote="quote" template-id="0" quote-id="0" client-id=""></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<div cla');
        });
 
        it('adds service', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().addService();
            expect($scope.quote.services.length).toEqual(2);
        });
 
        it('adds section', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().addSection();
            expect($scope.quote.sections.length).toEqual(3);
        });
    });
});
 
