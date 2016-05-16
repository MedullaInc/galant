
describe('clTaskList', function() {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('calendr.directives.clTaskList', function ($provide) {
            $provide.factory('Task', function ($q) {
                var Task = {};
                Task.query = function () {
                    return {$promise: $q.when([{}])};
                };
                return Task;
            });
        });
        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    var element;

    beforeEach(function() {
        element = $compile('<div cl-task-list="" assignee="0"></div>')($scope);
        $scope.$digest();
    });

    it('compiles', function () {
        expect(element.html().substring(0, 6)).toEqual('<table');
    });

    it('filters by assignee', function () {
        expect(element.isolateScope().byAssignee({assignee: 1})).toEqual(false);
        element.isolateScope().assignee = null;
        $scope.$digest();
        expect(element.isolateScope().byAssignee({assignee: 1})).toEqual(true);
    });
});

describe('clTaskAdd', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('calendr.services.clServices', function ($provide) {
            $provide.factory('Task', function ($q) {
                var Task = function () {
                };
                return Task;
            });
        });

        module('calendr.directives.clTaskAdd', function ($controllerProvider) {
            $controllerProvider.register('glFormController', function ($scope) {
                // Controller Mock
            });
        });

        module('staticNgTemplates');

        inject(function (_$rootScope_, _$compile_, _$injector_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    it('compiles without task', function () {
        $scope.projects = [{services: []}];
        element = $compile('<div cl-task-add="" projects="projects"></div>')($scope);
        $scope.$digest();
        expect(element.html().substring(0, 6)).toEqual('<form ');
    });

    var element;

    beforeEach(inject(function () {
    }));

    it('compiles', function () {
        $scope.projects = [{services: [{},{}]}, {id: 1, services: [{},{}]}, {id: 0}];
        $scope.task = {start: true, end: true, project: 1};
        element = $compile('<div cl-task-add="" projects="projects" task="task"></div>')($scope);
        $scope.$digest();
        expect(element.html().substring(0, 6)).toEqual('<form ');
    });

    it('changes project', function () {
        $scope.projects = [{services: [{},{}]}, {id: 1, services: [{},{}]}, {id: 0}];
        $scope.task = {start: true, end: true};
        element = $compile('<div cl-task-add="" projects="projects" task="task"></div>')($scope);
        $scope.$digest();
        element.isolateScope().projectChanged(0);
        element.isolateScope().projectChanged(1);
        expect(element.html().substring(0, 6)).toEqual('<form ');
    });

});