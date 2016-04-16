
describe('clTaskList', function() {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
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
            element = $compile('<div cl-task-list="" assignee="0"></div>')($scope);
            $scope.$digest();
        });

        it('compiles', function () {
            expect(element.html().substring(0, 6)).toEqual('<div c');
        });
    });
});