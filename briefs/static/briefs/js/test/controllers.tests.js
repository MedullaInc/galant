describe('brPopoverController', function () {
    var $rootScope;
    var $controller;
    var $window;
    var url = 'about:blank';
 
    beforeEach(function () {
        angular.module('briefs.services.brServices', []);
        angular.module('ngAnimate', []);
        module('briefs.services.brServices', function ($provide) {
            $provide.factory('Brief', function ($q) {
                var Brief = jasmine.createSpyObj('Brief', ['query', 'fields']);
 
                Brief.query.and.returnValue({$promise: $q.when([{id: 1}])});
                Brief.fields.and.returnValue({$promise: $q.when({})});
 
                return Brief;
            });
            $provide.factory('BriefTemplate', function ($q) {
                var BriefTemplate = jasmine.createSpyObj('BriefTemplate', ['query', 'fields']);
 
                BriefTemplate.query.and.returnValue({$promise: $q.when([{id: 1}])});
                BriefTemplate.fields.and.returnValue({$promise: $q.when({})});
 
                return BriefTemplate;
            });
        });
        module('briefs.controllers.brPopoverController', function ($provide) {
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
        $controller('brPopoverController', {$scope: $scope});
        $scope.init(url, url, 1);
        $rootScope.$apply();
        $scope.briefs = $scope.briefs;
    });
 
    it('sets addBriefURL', function () {
        expect($scope.addBriefUrl).toEqual(url);
    });
 
    it('generates addBriefRedirect redirect URL', function () {
        $scope.addBriefRedirect();
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
