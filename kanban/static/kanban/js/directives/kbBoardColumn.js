app = angular.module('kanban.directives.kbBoardColumn', [
    'as.sortable',
    'kanban.services.kbServices',
]);

app.directive('kbBoardColumn', ['KanbanCard', function (KanbanCard) {
    return {
        restrict: 'A',
        replace: true,
        scope: {
            items: '=?',
            statusIndex: '@',
            title: '@',
            clickFn: '&',
        },
        controller: ['$scope', function ($scope) {
            $scope.callback = $scope.clickFn();
            $scope.sortItems = function () {
                $scope.itemsSafe = $scope.itemsSafe.sort(function (a, b) { return a.card.yindex - b.card.yindex; });
            };

            if ($scope.items) {
                $scope.itemsSafe = $scope.items;
                $scope.sortItems();
            }

            $scope.updateCardIndex = function(items) {
                angular.forEach(items, function (it, idx) {
                    it.card.yindex = idx;
                    KanbanCard.update({id: it.card.id}, {yindex: it.card.yindex});
                });
            };

            $scope.dragControlListeners = {
                itemMoved: function (event) {
                    var item = event.source.itemScope.item;
                    var xidx = +event.dest.sortableScope.$parent.statusIndex;
                    item.status = xidx;
                    item.auto_pipeline = false;
                    item.$update({id: item.id});

                    $scope.updateCardIndex(event.dest.sortableScope.itemsSafe);
                    $scope.updateCardIndex(event.source.itemScope.itemsSafe);
                },
                orderChanged: function (event) {
                    $scope.updateCardIndex($scope.itemsSafe);
                }
            };

            $scope.$watchCollection('items', function(newValue, oldValue) {
                if (newValue) {
                    $scope.itemsSafe = newValue.filter(function (item) {
                        return +item.status == +$scope.statusIndex;
                    });
                    $scope.sortItems();
                }
            });
        }],
        templateUrl: '/static/kanban/html/kb_board_column.html',
        link: function ($scope) {
        }
    };
}]);