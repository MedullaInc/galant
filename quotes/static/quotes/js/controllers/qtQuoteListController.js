app = angular.module('quotes.controllers.qtQuoteListController', ['quotes.services.qtServices']);

app.controller('qtQuoteListController', ['$scope', '$http', '$window', '$uibModal', 'Quote', 'QuoteTemplate', 'Client',
    function($scope, $http, $window, $uibModal, Quote, QuoteTemplate, Client) {
        $scope.quotes = [];
        $scope.quoteStatus = [];
        $scope.quoteTemplates = [];
        $scope.clients = [];

        Quote.query().$promise.then(function(quotes) {
            $scope.quotes = quotes;
        });

        Client.query().$promise.then(function(clients) {
            $scope.clients = clients;
        });

        QuoteTemplate.query().$promise.then(function(quoteTemplates) {
            $scope.quoteTemplates = quoteTemplates;
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

        $scope.init = function(quoteDetailURL, addQuoteURL, quoteTemplateDetailURL) {
            $scope.quoteDetailURL = quoteDetailURL;
            $scope.addQuoteURL = addQuoteURL;
            $scope.quoteTemplateDetailURL = quoteTemplateDetailURL;
        };

        $scope.redirect = function(quoteID) {
            $window.location.href = $scope.quoteDetailURL + quoteID;
        };

        $scope.redirectTemplate = function(quoteTemplate) {
            $window.location.href = $scope.addQuoteURL + "?template_id=" + quoteTemplate.id + "&lang=" + quoteTemplate.languageSelection;
        };

        $scope.redirectTemplateDetail = function(quoteTemplate) {
            $window.location.href = $scope.quoteTemplateDetailURL + quoteTemplate.id
        };

        $scope.addQuoteRedirect = function() {
            $window.location.href = $scope.addQuoteURL;
        };

        $scope.languageSelection = function(quoteTemplate, lang) {
            quoteTemplate.languageSelection = lang;
        };


        $scope.dynamicPopover = {
            templateUrl: 'myPopoverTemplate.html',
        };

        $scope.animationsEnabled = true;

        $scope.open = function(size) {
            // Modal
            var modalInstance = $uibModal.open({
                animation: $scope.animationsEnabled,
                templateUrl: 'myModalContent.html',
                controller: 'qtQuoteListController',
                size: size,
                resolve: {
                    items: function() {
                        return $scope.items;
                    }
                }
            });

            modalInstance.result.then(function(selectedItem) {
                $scope.selected = selectedItem;
            });

        };

        $scope.toggleAnimation = function() {
            $scope.animationsEnabled = !$scope.animationsEnabled;
        };

        $scope.ok = function() {
            $uibModalInstance.close($scope.selected.item);
        };

        $scope.cancel = function() {
            $uibModalInstance.dismiss('cancel');
        };

    }

]);