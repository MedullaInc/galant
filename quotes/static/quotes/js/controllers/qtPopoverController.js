app = angular.module('quotes.controllers.qtPopoverController', ['ui.bootstrap', 'quotes.services.qtServices']);

app.controller('qtPopoverController', ['$scope', '$http', '$window', '$uibModal', 'Quote', 'QuoteTemplate',
    function($scope, $http, $window, $uibModal, Quote, QuoteTemplate) {

    Quote.query().$promise.then(function(quotes) {
        $scope.quotes = quotes;
    });

    QuoteTemplate.query().$promise.then(function(quoteTemplates) {
        $scope.quoteTemplates = quoteTemplates;
    });    

	$scope.dynamicPopover = {
		templateUrl: 'myPopoverTemplate.html',
	};

    $scope.init = function(addQuoteURL, quoteTemplateDetailURL) {
        $scope.addQuoteURL = addQuoteURL;
    };

    $scope.redirectTemplate = function(quoteTemplate) {
        $window.location.href = '/en/quote/add/' + "?template_id=" + quoteTemplate.id + "&lang=" + quoteTemplate.languageSelection;
    };

    $scope.addQuoteRedirect = function() {
        $window.location.href = $scope.addQuoteURL;
    };

    $scope.languageSelection = function(quoteTemplate, lang) {
        quoteTemplate.languageSelection = lang;
    };

	$scope.open = function () {
		$scope.modalInstance = $uibModal.open({
			animation: true,
			templateUrl: 'myModalContent.html',
			controller: 'qtPopoverController',
			resolve: {}
		});
	};

}

]);