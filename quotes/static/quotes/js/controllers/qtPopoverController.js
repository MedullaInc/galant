app = angular.module('quotes.controllers.qtPopoverController', ['ngAnimate', 'ui.bootstrap', 'quotes.services.qtServices']);

app.controller('qtPopoverController', ['$scope', '$http', '$window', '$rootScope', '$uibModal', 'Quote', 'QuoteTemplate',
    function ($scope, $http, $window, $rootScope, $uibModal, Quote, QuoteTemplate) {

        if ($rootScope.quoteTemplates) {
            $scope.quoteTemplates = $rootScope.quoteTemplates;
        } else {
            QuoteTemplate.query().$promise.then(function (response) {
                $scope.quoteTemplates = response;
            });
        }

        $scope.init = function (addQuoteURL, currentLanguage, clientId) {
            $scope.addQuoteURL = addQuoteURL;
            $scope.currentLanguage = currentLanguage;
            $scope.selectedLanguage = currentLanguage;
            $scope.clientId = clientId;
        };

        $scope.dynamicPopover = {
            templateUrl: 'addQuotePopoverTemplate.html',
        };

        $scope.redirectTemplate = function (quoteTemplate) {
            // In case there was no selection
            if (!quoteTemplate.languageSelection) {
                quoteTemplate.languageSelection = $scope.currentLanguage;
            }
            var ref = $scope.addQuoteURL + "?template_id=" + quoteTemplate.id + "&lang=" + quoteTemplate.languageSelection;
            if ($scope.clientId)
                ref += '&client_id=' + $scope.clientId;
            $window.location.href = ref;
        };

        $scope.addQuoteRedirect = function () {
            var ref = $scope.addQuoteURL;
            if ($scope.clientId)
                ref += '?client_id=' + $scope.clientId;
            $window.location.href = ref;
        };

        $scope.languageSelection = function (quoteTemplate, lang) {
            quoteTemplate.languageSelection = lang;
        };

        $scope.open = function () {
            $scope.modalInstance = $uibModal.open({
                scope: $scope,
                animation: true,
                templateUrl: 'quoteTemplateModalContent.html',
                controller: 'qtPopoverController',
            });
            return 0;
        };

    }

]);