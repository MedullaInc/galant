app = angular.module('calendr.directives.clTaskList', [
    'calendr.services.clServices',
    'smart-table',
]);

app.directive('clTaskList', [function () {
    return {
        restrict: 'A',
        scope: {
            tasks: '=',
            assignee: '@',
            editTaskFn: '&',
        },
        controller: ['$scope', function ($scope) {
            $scope.editTask = $scope.editTaskFn();
            $scope.byAssignee = function (task) {
                if ($scope.assignee)
                    return task.assignee == $scope.assignee;
                else
                    return true;
            };
        }],
        templateUrl: '/static/calendr/html/cl_task_list.html',
        link: function ($scope) {
        }
    };
}]);