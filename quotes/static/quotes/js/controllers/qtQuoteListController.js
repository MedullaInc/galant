app = angular.module('quotes.controllers.qtQuoteListController', ['quotes.services.qtServices']);

app.controller('qtQuoteListController', ['$scope', '$http', '$window', '$uibModal', 'Quote', 'QuoteTemplate', 'Client',
    function($scope, $http, $window, $uibModal, Quote, QuoteTemplate, Client) {
        $scope.quotes = [];
        $scope.quoteStatus = [];
        $scope.clients = [];

        Quote.query().$promise.then(function(quotes) {
            $scope.quotes = quotes;
        });

        QuoteTemplate.query().$promise.then(function(quoteTemplates) {
            $scope.quoteTemplates = quoteTemplates;
        });    

        Client.query().$promise.then(function(clients) {
            $scope.clients = clients;
        });

        Quote.fields().$promise.then(function(fields) {
            for (var key in fields.status) {
                // must create a temp object to set the key using a variable
                var tempObj = {};
                tempObj[key] = fields.status[key];
                $scope.quoteStatus.push({
                    value: key,
                    text: tempObj[key]
                });
            }
        });

        $scope.init = function(quoteDetailURL) {
            $scope.quoteDetailURL = quoteDetailURL;
        };

        $scope.redirect = function(id) {
            $window.location.href = $scope.quoteDetailURL + id
        };

    }

]);