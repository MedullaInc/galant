app = angular.module('gallant.directives.glClientAdd', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.controllers.glFormController',
    'gallant.directives.glForm',
]);

app.directive('glClientAdd', ['$window', 'Client', 'LANGUAGES', 'glConstants',
    function ($window, Client, LANGUAGES, glConstants) {
    return {
        restrict: 'A',
        scope: {
            onSuccess: '&',
        },
        controller: ['$scope', function ($scope) {
            $scope.languages = LANGUAGES;
            $scope.client = new Client();
            $scope.client.notes = [];
            $scope.client.status = glConstants.ClientStatus.Potential;
            $scope.object = $scope.client;
            $scope.objectEndpoint = Client;

            $scope.clientSaved = $scope.onSuccess();
        }],
        templateUrl: '/static/gallant/html/gl_client_add.html',
        link: function ($scope) {
        }
    };
}]);