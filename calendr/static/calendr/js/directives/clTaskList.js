app = angular.module('calendr.directives.clTaskList', [
    'gallant.directives.glAddModal',
    'calendr.directives.clTaskAdd',
    'calendr.services.clServices',
    'smart-table',
]);

app.directive('clTaskList', ['Task', 'clConstants', function (Task) {
    return {
        restrict: 'A',
        scope: {
            tasks: '=?',
            tasksLoaded: '=?',
            assignee: '@',
            editTaskFn: '&',
        },
        controller: ['$scope', function ($scope) {
            if (!$scope.tasks) {
                Task.query().$promise.then(function (response) {
                    $scope.tasks = response;
                    $scope.tasksLoaded = true;
                });
            }

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