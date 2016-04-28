app = angular.module('kanban.directives.kbBoardColumn', [
    'as.sortable',
]);

app.directive('kbBoardColumn', function () {
    return {
        restrict: 'A',
        replace: true,
        scope: {
            items: '=?',
            statusIndex: '@',
            title: '@',
        },
        controller: ['$scope', function ($scope) {
            if (!$scope.items)
                $scope.items = [];

            $scope.filterItems = function () {
                return $scope.items.filter(function (item) { return +item.status == +$scope.statusIndex; });
            };

            $scope.dragControlListeners = {
                itemMoved: function (event) {
                    var item = event.source.itemScope.item;
                    item.status = +event.dest.sortableScope.$parent.statusIndex;
                    item.auto_pipeline = false;
                    item.$update({id: item.id});
                }
            };
        }],
        templateUrl: '/static/kanban/html/kb_board_column.html',
        link: function ($scope) {
        }
    };
});