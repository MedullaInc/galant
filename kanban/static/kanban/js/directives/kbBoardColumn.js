app = angular.module('kanban.directives.kbBoardColumn', [
    'as.sortable',
]);

app.directive('kbBoardColumn', function () {
    return {
        restrict: 'A',
        replace: true,
        scope: {
            items: '=?',
            title: '@',
        },
        controller: ['$scope', function ($scope) {
            if (!$scope.items)
                $scope.items = [];
        }],
        templateUrl: '/static/kanban/html/kb_board_column.html',
        link: function ($scope) {
        }
    };
});