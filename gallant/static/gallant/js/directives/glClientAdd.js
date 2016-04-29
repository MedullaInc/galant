app = angular.module('gallant.directives.glClientAdd', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.controllers.glFormController',
    'gallant.directives.glForm',
]);

app.directive('glClientAdd', ['$window', 'Client', 'LANGUAGES', function ($window, Client, LANGUAGES) {
    return {
        restrict: 'A',
        scope: {
            clients: '=',
        },
        controller: ['$scope', function ($scope) {
            $scope.languages = LANGUAGES;
            $scope.client = new Client();
            $scope.client.notes = [];
            $scope.object = $scope.client;
            $scope.objectEndpoint = Client;

            $scope.clientSaved = function (client) {
                console.log('here');
            }
        }],
        templateUrl: '/static/gallant/html/gl_client_add.html',
        link: function ($scope) {
        }
    };
}]);