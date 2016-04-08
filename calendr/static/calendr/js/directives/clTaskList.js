app = angular.module('calendr.directives.clTaskList', [
    'calendr.services.clServices',
]);

app.directive('clTaskList', ['$window','Task', function ($window, Task) {
    return {
        restrict: 'A',
        scope: {
        },
        controller: ['$scope', function ($scope) {}],
        templateUrl: '/static/calendr/html/cl_task_list.html',
        link: function ($scope) {
        }
    };
}]);