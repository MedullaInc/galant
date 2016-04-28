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
                console.log($scope.items);
                console.log($scope.statusIndex);
                return $scope.items.filter(function (item) { return +item.status % 10 == +$scope.statusIndex; });
            }
        }],
        templateUrl: '/static/kanban/html/kb_board_column.html',
        link: function ($scope) {
        }
    };
});