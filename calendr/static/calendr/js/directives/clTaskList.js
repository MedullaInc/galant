app = angular.module('calendr.directives.clTaskList', [
    'calendr.services.clServices',
    'smart-table',
]);

app.directive('clTaskList', ['$window','Task', function ($window, Task) {
    return {
        restrict: 'A',
        scope: {
            assignee: '@',
        },
        controller: ['$scope', function ($scope) {
            var options = {};
            if ($scope.assignee)
                options.assignee = $scope.assignee;

            Task.query(options).$promise.then(function (response) {
                $scope.tasks = response;
            });
        }],
        templateUrl: '/static/calendr/html/cl_task_list.html',
        link: function ($scope) {
        }
    };
}]);