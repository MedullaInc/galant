describe('qtForm', function () {
    var $rootScope;
    var $compile;
    var $scope;
    var $window;

    beforeEach(function () {
        module('quotes.directives.qtForm');
        module('quotes.directives.qtClientForm');
        module('quotes.directives.qtServiceTable');
        module('quotes.directives.qtSectionTable');
        module('quotes.filters.qtCutFilter');
        module('staticNgTemplates');
        angular.module('ngAnimate', []);
        angular.module('as.sortable', []);
        angular.module('ui.bootstrap', []); 

        angular.module('quotes.services.qtServices', []);
        module('quotes.services.qtServices', function ($provide) { 
            $provide.factory('Quote', function ($q) {
                var Quote = function () { return {id: 0}; };
                Quote.get = function () { return {$promise: $q.when({id: 0, sections: [{}], ervices: [{cost: [{amount: 0, currency:"USD"}]}]})}; };
                Quote.getUser = function () { return {$promise: $q.when({id: 0, sections: [{}], ervices: [{cost: [{amount: 0, currency:"USD"}]}]})}; };
                Quote.update = function () { return {$promise: $q.when({id: 0})}; };
                Quote.fields = function () { return {$promise: $q.when({status: ['status', 'status'], language: ['language', 'language']})}; };
                return Quote;
            });

            $provide.factory('QuoteTemplate', function ($q) {
                var QuoteTemplate = function () { return {id: 0}; };
                QuoteTemplate.get = function () { return {$promise: $q.when({id: 0, languages: [], quote: {
                    id: 0,
                    sections: [{}],
                    services: [{cost: [{amount: 0, currency:"USD"}]}],
                }})}; };
                return QuoteTemplate;
            });

            $provide.factory('Client', function ($q) {
                var Client = jasmine.createSpyObj('Client', ['get', 'fields']);
                Client.get.and.returnValue({$promise: $q.when([{id: 0}])});
                return Client;
            });

            $provide.factory('Section', function ($q) {
                var Section = function () { return {id: 0}; };
                Section.get = function () { return {$promise: $q.when({id: 0})}; };
                Section.update = function () { return {$promise: $q.when({type: ['type', 'type']})};  };
                return Section;
            });

            $provide.factory('Service', function ($q) {
                var Service = function () { return {id: 0}; };
                Service.get = function () { return {$promise: $q.when({id: 0})}; };
                Service.fields = function () { return {$promise: $q.when({type: ['type', 'type']})};  };
                Service.update = function () { return {$promise: $q.when({type: ['type', 'type']})};  };
                return Service;
            });

        });
        module('quotes.directives.qtForm', function ($provide) {
            $provide.value('$uibModal', {open: function () {}});
            $provide.value('$window', {location: {href: null}});
        });
        inject(function (_$rootScope_, _$compile_, _$window_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
            $window = _$window_;
        });
 
        $rootScope.language = 'en';
        $rootScope.text = {en: 'sadf'}
        $scope = $rootScope.$new();
    });


  describe('qtQuoteForm', function () {
  
    it('has a cut filter', inject(function($filter) {
        expect($filter('cut')).not.toBeNull();
    }));

    it("should trim the string to 5 chars ", inject(function (cutFilter) {
        expect(cutFilter("xxxxxxxxxx",true,5,"").length).toEqual(5);
    }));

    it("test lastspace ", inject(function (cutFilter) {
        expect(cutFilter("xxx xxxxxxx ",true,5,"").length).toEqual(3);
    }));

    it("exceed max ", inject(function (cutFilter) {
        expect(cutFilter("xxx xxxxxxx ",true,15,"").length).toEqual(12);
    }));

  });


  describe('qtQuoteForm', function () {

        beforeEach(function () {
            $scope.quote = {type: 'Quote'};
            $scope.quoteTemplate = {type: 'QuoteTemplate'};
            $scope.language = 'en';
            $scope.endpoint = $scope.quote;
            $scope.modalInstance = {};
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

        it('check client', function () {
            /* TODO */
            pending();
            
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote" ></div>')($scope);
            $scope.$digest();
            var expected = element.isolateScope().checkClient();
            expect(expected).toEqual("Plase select a client");
        });

        it('adds service (scratch)', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form quote="quote" ></div>')($scope);
            $scope.$digest();
            element.isolateScope().open();
            element.isolateScope().addService();
            expect($scope.quote.services.length).toEqual(2);
        });
 
        it('adds section', function () {
            var element = $compile('<div qt-quote-form quote="quote" ></div>')($scope);
            $scope.$digest();
            element.isolateScope().addSection();
            expect($scope.quote.sections.length).toEqual(3);
        });

        it('changes language', function () {
            $scope.quote = {};
            var element = $compile('<div qt-quote-form  quote-template="quoteTemplate" is-template="true"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().changeLanguage(["en","en"]);
            expect($scope.language.length).toEqual(2);
        });

        it('adds language', function () {
            var element = $compile('<div qt-quote-form quote-template="quoteTemplate" bool-template="True" template-id="quoteTemplate.id"></div>')($scope);
            $scope.$digest();

            element.isolateScope().addLanguage({'code': 'es', 'name': 'Spanish'});
            expect(element.isolateScope().quoteTemplate.languages.length).toEqual(2);
        });

        it('sets language', function () {
            var element = $compile('<div qt-quote-form quote-template="quoteTemplate" bool-template="True"></div>')($scope);
            $scope.$digest();

            element.isolateScope().setLanguage('en');
            expect(element.isolateScope().language).toEqual('en');
        });

        it('show rowform', function () {
            $scope.quote = {};
            $scope.rowform = {$show: function(){}};
            var element = $compile('<div qt-quote-form quote="quote"></div>')($scope);
            $scope.$digest();
 
            element.isolateScope().showRowForm($scope.rowform);
            expect($scope.quote.sections.length).toEqual(2);
        });

        it('adds onload function', function () {
            var element = $compile('<div qt-quote-form quote="quote" id-type="token"></div>')($scope);
            $scope.$digest();
            var result = $window.onbeforeunload();
            expect(result).not.toBeNull();
            $window.onbeforeunload = null; // remove so browser doesn't get stuck
        });


    });


    describe('qtClientForm', function () {

        it('compiles', function () {
            var element = $compile('<div qt-client id-type="token"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 4)).toEqual('<div');
        });

        it('adds onbeforeunload function', function () {
            var element = $compile('<div qt-client id-type="token"></div>')($scope);
            $scope.$digest();
            var result = $window.onbeforeunload();
            expect(result).not.toBeNull();
            $window.onbeforeunload = null; // remove so browser doesn't get stuck
        });

    });


    describe('qtServiceTable', function () {

        it('compiles', function () {
            var element = $compile('<div qt-service-table></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 4)).toEqual('<div');
        });

        it('remove service', function () {
            $scope.quote = { "sections": [],"services": []};
            $scope.insertedService = {cost: {amount: "0", currency: "USD"}};
            $scope.quote.services.push($scope.insertedService);

            var element = $compile('<div qt-service-table></div>')($scope);
            $scope.$digest();
            element.scope().removeService();
            expect($scope.quote.services.length).toEqual(0);
        });

        it('show service', function () {
            $scope.quote = {};
            $scope.service = {id:0};
            $scope.idType = "token";
            var element = $compile('<div qt-service-table></div>')($scope);
            $scope.$digest();
 
            element.scope().showService($scope.service);
            expect($scope.service).toBeDefined();
        });

    });
    

    describe('qtSectionTable', function () {

        it('compiles', function () {
            var element = $compile('<div qt-section-table></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 4)).toEqual('<div');
        });

        it('show section', function () {
            $scope.quote = {};
            $scope.section = {id:0};
            $scope.idType = "token";
            var element = $compile('<div qt-section-table></div>')($scope);
            $scope.$digest();
            element.scope().showSection($scope.section);
            expect($scope.section).toBeDefined();
        });

        it('remove section', function () {
            $scope.quote = { "sections": [],"services": []};
            $scope.section = {id:0};
            $scope.quote.sections.push($scope.section);

            var element = $compile('<div qt-section-table></div>')($scope);
            $scope.$digest();
            element.scope().removeSection();
            expect($scope.quote.sections.length).toEqual(0);
        });

    });
    
});
 
