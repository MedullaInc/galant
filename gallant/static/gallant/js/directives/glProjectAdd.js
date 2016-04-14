app = angular.module('gallant.directives.glProjectAdd', [
    'ui.bootstrap',
    'gallant.services.glServices',
]);

app.directive('glProjectAdd', ['$window', 'Project', function ($window, Project) {
    return {
        restrict: 'A',
        scope: {
            project: '=',
            endpoint: '=',
            submit: '&'
        },
        controller: ['$scope', function ($scope) {
            $scope.project = new Project();
            $scope.project.notes = [];
            $scope.endpoint = Project;
            $scope.submitForm = $scope.submit();

            Project.fields({}).$promise.then(function (fields) {
                $scope.statusChoices = fields.status;
            });
        }],
        templateUrl: '/static/gallant/html/gl_project_add.html',
        link: function ($scope) {
        }
    };
}]);