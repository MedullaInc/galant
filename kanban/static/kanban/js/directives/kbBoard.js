app = angular.module('kanban.directives.kbBoard', [
]);

app.directive('kbBoard', function () {
    return {
        restrict: 'A',
        scope: {
        },
        controller: ['$scope', function ($scope) {}],
        templateUrl: '/static/kanban/html/kb_board.html',
        link: function ($scope) {
        }
    };
});