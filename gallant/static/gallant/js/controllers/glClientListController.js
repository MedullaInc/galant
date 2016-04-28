app = angular.module('gallant.controllers.glClientListController', ['gallant.services.glServices', 'kanban.directives.kbBoardColumn']);

app.controller('glClientListController', ['$scope', '$http', '$window', 'Client', 'glConstants',
    function ($scope, $http, $window, Client, glConstants) {
        $scope.glConstants = glConstants;

        Client.query().$promise.then(function (clients) {
            $scope.clientsSafe = clients;
/*            $scope.potential = clients.filter(
                function (c) { return (+c.status) % 10 == glConstants.ClientStatus.Potential; });
            $scope.quoted = clients.filter(
                function (c) { return (+c.status) % 10 == glConstants.ClientStatus.Quoted; });
            $scope.projectUnderway = clients.filter(
                function (c) { return (+c.status) % 10 == glConstants.ClientStatus.ProjectUnderway; });
            $scope.pendingPayment = clients.filter(
                function (c) { return (+c.status) % 10 == glConstants.ClientStatus.PendingPayment; });
            $scope.closed = clients.filter(
                function (c) { return (+c.status) % 10 == glConstants.ClientStatus.Closed; });*/
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