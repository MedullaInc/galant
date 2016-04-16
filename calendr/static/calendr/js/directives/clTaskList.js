app = angular.module('calendr.directives.clTaskList', [
    'calendr.services.clServices',
    'smart-table',
]);

app.directive('clTaskList', ['$window','Task', function ($window, Task) {
    return {
        restrict: 'A',
        scope: {
            byUser: '@',
        },
        controller: ['$scope', function ($scope) {
            Task.query().$promise.then(function (response) {
                $scope.tasks = response;
            });
        }],
        templateUrl: '/static/calendr/html/cl_task_list.html',
        link: function ($scope) {
        }
    };
}]);