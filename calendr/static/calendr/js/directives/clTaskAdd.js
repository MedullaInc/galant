app = angular.module('calendr.directives.clTaskAdd', [
    'ui.bootstrap',
    'calendr.services.clServices',
    'gallant.directives.glForm',
    'gallant.directives.glMultiDropdown',
]);

app.directive('clTaskAdd', ['$window', 'Task', function ($window, Task) {
    return {
        restrict: 'A',
        scope: {
            task: '=?',
            users: '=?',
            projects: '=?',
            assignee: '@',
            onSuccess: '&',
            onDeleted: '&',
        },
        controller: ['$scope', function ($scope) {

            if (!$scope.task) {
                $scope.task = new Task();
                $scope.task.assignee = $scope.assignee;
                $scope.task.daily_estimate = 0;
            }

            if (!$scope.task.services)
                $scope.task.services = [];

            if ($scope.task.start) {
                $scope.task.start = new Date($scope.task.start);
            } else {
                $scope.task.start = new Date();
            }

            if ($scope.task.end) {
                $scope.task.end = new Date($scope.task.end);
            } else {
                $scope.task.end = new Date();
            }

            if ($scope.projects.length && $scope.projects[0].services.length) {
                $scope.availableServices = $scope.projects[0].services;
            }

            $scope.project = $scope.projects.find(function (p) {
                return p.id == $scope.task.projectId
            });

            if ($scope.project && $scope.project.services.length) {
                $scope.availableServices = $scope.project.services;
            }

            if ($scope.task.project) {
                $scope.project = $scope.projects.find(function (p) {
                    return p.id == $scope.task.project
                });
                $scope.availableServices = $scope.project.services;
            }

            $scope.projectChanged = function (projectId) {
                $scope.project = $scope.projects.find(function (p) {
                    return p.id == projectId
                });
                if ($scope.project && $scope.project.services)
                    $scope.availableServices = $scope.project.services;
                else
                    $scope.availableServices = [];
                $scope.task.services = [];
            };

            $scope.objectEndpoint = Task;
            $scope.object = $scope.task;

            $scope.taskSaved = $scope.onSuccess();
            $scope.deleteTask = $scope.onDeleted();

        }],
        templateUrl: '/static/calendr/html/cl_task_add.html',
        link: function ($scope) {
        }
    };
}]);