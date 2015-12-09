app = angular.module('gallant.controllers.glClientListController', ['gallant.services.glServices']);

app.controller('glClientListController', ['$scope', '$http', '$window', 'Client',
    function ($scope, $http, $window, Client) {
        $scope.clients = [];

        Client.query().$promise.then(function (clients) {
            $scope.clientsSafe = clients;
        });

        Client.fields().$promise.then(function (fields) {
            $scope.clientFields = fields;
        });

        $scope.init = function(clientDetailURL) {
            $scope.clientDetailURL = clientDetailURL;
        };

        $scope.redirect = function(clientID) {
            $window.location.href = $scope.clientDetailURL + clientID;
        };

        $scope.updateLastContacted = function(rowIndex) {
            var client = $scope.clients[rowIndex];
            var last_contacted = (new Date()).toISOString();
            Client.update({id: client.id, last_contacted: last_contacted})
                .$promise.then(function (response) {
                client.last_contacted = last_contacted;
            });
        };
    }
]);