app = angular.module('gallant.directives.glProjectAdd', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glMultiDropdown',
    'quotes.services.qtServices',
]);

app.directive('glProjectAdd', ['$window', 'Project', 'Quote', function ($window, Project, Quote) {
    return {
        restrict: 'A',
        scope: {
            project: '=',
            endpoint: '=',
            projects: '=',
            modal: '=',
            submit: '&',
        },
        controller: ['$scope', function ($scope) {
            $scope.project = new Project();
            $scope.project.notes = [];
            $scope.project.quotes = [];
            $scope.endpoint = Project;
            $scope.submitForm = $scope.submit();
            $scope.quotes = [];

            Project.fields({}).$promise.then(function (fields) {
                $scope.statusChoices = fields.status;
            });

            Quote.query({unlinked: true}).$promise.then(function (response) {
                $scope.quotes = response;
            });
        }],
        templateUrl: '/static/gallant/html/gl_project_add.html',
        link: function ($scope) {
        }
    };
}]);