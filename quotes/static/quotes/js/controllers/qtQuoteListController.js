app = angular.module('quotes.controllers.qtQuoteListController', ['quotes.services.qtServices','ngAnimate']);

app.controller('qtQuoteListController', ['$scope', '$http', '$window', 'Quote', 'QuoteTemplate', 'Client',
    function($scope, $http, $window, Quote, QuoteTemplate, Client) {
        $scope.quotes = [];
        $scope.quoteStatus = [];
        $scope.clients = [];

        $scope.init = function(quoteDetailURL, currentLanguage) {
            $scope.quoteDetailURL = quoteDetailURL;
            $scope.currentLanguage = currentLanguage;
        };

        Quote.fields().$promise.then(function (fields) {
            $scope.quoteStatus = fields.status;
        });

        Quote.query().$promise.then(function(quotes) {
            $scope.quotesSafe = quotes;
        });

        QuoteTemplate.query().$promise.then(function(quoteTemplates) {
            $scope.quoteTemplates = quoteTemplates;
        });    

        Client.query().$promise.then(function(clients) {
            $scope.clients = clients;
        });

        $scope.redirect = function(id) {
            $window.location.href = $scope.quoteDetailURL + id;
        };

    }

]);