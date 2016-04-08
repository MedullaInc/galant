
describe('clTaskList', function() {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('calendr.services.clServices', function($provide) {
            $provide.factory('Task', function ($q) {
                var Task = {};
                return Task;
            });
        });

        module('calendr.directives.clTaskList');
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('clTaskList', function() {

        var element;

        beforeEach(function() {
            element = $compile('<div cl-task-list=""></div>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });
    });
});