describe('kbBoardColumn', function() {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('kanban.directives.kbBoardColumn', function ($provide) {
/*            $provide.factory('Task', function ($q) {
                var Task = {};
                Task.query = function () {
                    return {$promise: $q.when([{}])};
                };
                return Task;
            });*/
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
        $scope.items = [{}, {}];
        element = $compile('<div kb-board-column items="items"></div>')($scope);
        $scope.$digest();
    });

    it('compiles', function () {
        expect(element.html().trim().substring(0, 6)).toEqual('<div c');
    });

    it('moves item', function () {
        element.isolateScope().dragControlListeners.itemMoved({
            source: {itemScope: {item: {$update: function () {}}}},
            dest: {sortableScope: {$parent: {statusIndex: {}}}}
        });
    });
});
