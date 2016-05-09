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
            onSuccess: '&',
        },
        controller: ['$scope', function ($scope) {
            $scope.task = new Task();
            $scope.objectEndpoint = Task;
            $scope.object = $scope.task;

            $scope.taskSaved = $scope.onSuccess();
        }],
        templateUrl: '/static/calendr/html/cl_task_add.html',
        link: function ($scope) {
        }
    };
}]);