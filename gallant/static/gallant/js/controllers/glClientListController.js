app = angular.module('gallant.controllers.glClientListController', ['gallant.services.glServices']);

app.controller('glClientListController', ['$scope', '$http', '$window', 'Client',
    function ($scope, $http, $window, Client) {
        Client.query().$promise.then(function (clients) {
            $scope.clients = clients;
        });

        $scope.init = function(clientDetailURL) {
            $scope.clientDetailURL = clientDetailURL;
        }

        $scope.redirect = function(clientID) {
            $window.location.href = $scope.clientDetailURL + clientID;
        }
    }
]);