app = angular.module('gallant.controllers.glClientListController', ['gallant.services.glServices', 'kanban.directives.kbBoardColumn']);

app.controller('glClientListController', ['$scope', '$http', '$window', 'Client',
    function ($scope, $http, $window, Client) {
        Client.query().$promise.then(function (clients) {
            $scope.clientsSafe = clients;
            $scope.notQuoted = clients.filter(function (c) { return c.status.indexOf('Pre_Quote') >= 0; });
            $scope.quoted = clients.filter(function (c) { return c.status.indexOf('Quoted') >= 0; });
            $scope.projectUnderway = clients.filter(function (c) { return c.status.indexOf('Project_Underway') >= 0; });
            $scope.pendingPayment = clients.filter(function (c) { return c.status.indexOf('Pending_Payment') >= 0; });
            $scope.closed = clients.filter(function (c) { return c.status.indexOf('Closed') >= 0; });
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