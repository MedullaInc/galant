app = angular.module('quotes.controllers.qtQuoteListController', ['quotes.services.qtServices', 'gallant.services.glServices', 'ngAnimate', 'kanban.directives.kbBoardColumn']);

app.controller('qtQuoteListController', ['$scope', '$http', '$window', '$rootScope',
    'Quote', 'QuoteTemplate', 'qtConstants',
    function ($scope, $http, $window, $rootScope, Quote, QuoteTemplate, qtConstants) {
        $scope.qtConstants = qtConstants;
        $scope.quoteStatus = [];
        $scope.clients = [];

        $scope.init = function (quoteDetailURL, currentLanguage, clientId) {
            $scope.quoteDetailURL = quoteDetailURL;
            $scope.currentLanguage = currentLanguage;

            var options = clientId ? {client_id: clientId} : {};

            Quote.query(options).$promise.then(function (quotes) {
                $scope.quotesSafe = quotes;
                $scope.quotesLoaded = true;

                angular.forEach(quotes, function (quote) {
                    quote.kanban_card_description = quote.client_name;
                });

            });
        };

        Quote.fields().$promise.then(function (fields) {
            $scope.quoteStatus = fields.status;
        });

        QuoteTemplate.query().$promise.then(function (quoteTemplates) {
            $scope.quoteTemplates = quoteTemplates;
            $rootScope.quoteTemplates = quoteTemplates;
        });

        $scope.redirect = function (quote) {
            $window.location.href = $scope.quoteDetailURL + quote.id;
        };

    }

]);