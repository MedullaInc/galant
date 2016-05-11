describe('kbBoardColumn', function() {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('kanban.directives.kbBoardColumn', function ($provide) {
            $provide.factory('KanbanCard', function ($q) {
                var KanbanCard = {};
                KanbanCard.update = function () {};
                return KanbanCard;
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
        $scope.items = [{status: 0, card: {yindex: 0}}, {status: 0, card: {yindex: 1}}];
        element = $compile('<div kb-board-column items="items" status-index="0"></div>')($scope);
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

    it('updates index', function () {
        element.isolateScope().dragControlListeners.orderChanged({
            source: {itemScope: {item: {$update: function () {}}}},
            dest: {sortableScope: {$parent: {statusIndex: {}}}}
        });
    });
});
