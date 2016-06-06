app = angular.module('gallant.directives.glProjectAdd', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glForm',
    'gallant.directives.glFormElements',
    'gallant.directives.glMultiDropdown',
    'quotes.services.qtServices',
]);

app.directive('glProjectAdd', ['$window', 'Project', 'Quote', 'Client',
        function ($window, Project, Quote, Client) {
    return {
        restrict: 'A',
        scope: {
            project: '=?',
            quoteId: '@',
            language: '@',
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

            Client.query().$promise.then(function (response) {
                $scope.clients = response;
            });

            $scope.projectSaved = $scope.onSuccess();
        }],
        templateUrl: '/static/gallant/html/gl_project_add.html',
        link: function ($scope) {
        }
    };
}]);