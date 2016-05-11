app = angular.module('gallant.controllers.glClientListController', ['gallant.services.glServices',
    'gallant.directives.glAddModal', 'kanban.directives.kbBoardColumn']);

app.controller('glClientListController', ['$scope', '$http', '$window', 'Client', 'glConstants',
    function ($scope, $http, $window, Client, glConstants) {
        $scope.glConstants = glConstants;

        Client.query().$promise.then(function (clients) {
            $scope.clientsSafe = clients;
            $scope.clientsLoaded = true;
        });

        Client.fields().$promise.then(function (fields) {
            $scope.clientFields = fields;
        });

        $scope.init = function (clientDetailURL) {
            $scope.clientDetailURL = clientDetailURL;
        };

        $scope.redirect = function (client) {
            $window.location.href = $scope.clientDetailURL + client.id;
        };

        $scope.updateLastContacted = function (rowIndex) {
            var client = $scope.clients[rowIndex];
            var last_contacted = (new Date()).toISOString();
            Client.update({id: client.id, last_contacted: last_contacted})
                .$promise.then(function (response) {
                client.last_contacted = last_contacted;
            });
        };

        $scope.clientSaved = function (client) {
            $scope.clientsSafe.push(client);
            $scope.modalInstance.dismiss('cancel');
        };
    }
]);