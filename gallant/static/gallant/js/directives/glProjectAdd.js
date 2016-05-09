app = angular.module('gallant.directives.glProjectAdd', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glForm',
    'gallant.directives.glMultiDropdown',
    'quotes.services.qtServices',
]);

app.directive('glProjectAdd', ['$window', 'Project', 'Quote', function ($window, Project, Quote) {
    return {
        restrict: 'A',
        scope: {
            onSuccess: '&',
        },
        controller: ['$scope', function ($scope) {
            $scope.project = new Project();
            $scope.project.notes = [];
            $scope.project.quotes = [];
            $scope.objectEndpoint = Project;
            $scope.object = $scope.project;
            $scope.quotes = [];

            Project.fields({}).$promise.then(function (fields) {
                $scope.statusChoices = fields.status;
            });

            Quote.query({unlinked: true}).$promise.then(function (response) {
                $scope.quotes = response;
            });

            $scope.projectSaved = $scope.onSuccess();
        }],
        templateUrl: '/static/gallant/html/gl_project_add.html',
        link: function ($scope) {
        }
    };
}]);