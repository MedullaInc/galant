app = angular.module('gallant.directives.glProjectAdd', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glForm',
    'gallant.directives.glFormElements',
    'gallant.directives.glMultiDropdown',
    'quotes.services.qtServices',
]);

app.directive('glProjectAdd', ['$window', 'Project', 'Quote', function ($window, Project, Quote) {
    return {
        restrict: 'A',
        scope: {
            project: '=?',
            quoteId: '@',
            onSuccess: '&',
        },
        controller: ['$scope', function ($scope) {
            if (!$scope.project) {
                $scope.project = new Project();
                $scope.project.notes = [];
                $scope.project.quotes = [];
                $scope.project.services = [];
            }

            $scope.objectEndpoint = Project;
            $scope.object = $scope.project;
            $scope.quotes = [];

            if ($scope.quoteId) {
                $scope.project.quotes.push(+$scope.quoteId);
            }

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