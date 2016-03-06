app = angular.module('quotes.controllers.qtQuoteTemplateListController', ['quotes.services.qtServices']);

app.controller('qtQuoteTemplateListController', ['$scope', '$window', 'QuoteTemplate',
    function($scope, $window, QuoteTemplate) {
        
        $scope.init = function(quoteDetailURL, currentLanguage) {
            $scope.quoteDetailURL = quoteDetailURL;
            $scope.currentLanguage = currentLanguage;
        };

        $scope.redirect = function(id) {
            $window.location.href = $scope.quoteDetailURL + id;
        };

        QuoteTemplate.query().$promise.then(function(quoteTemplates) {
            $scope.quoteTemplates = quoteTemplates;
        });    

    }

]);