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

	$scope.animationsEnabled = true;

	$scope.open = function (size) {

		var modalInstance = $uibModal.open({
			animation: $scope.animationsEnabled,
			templateUrl: 'myModalContent.html',
			controller: 'qtPopoverController',
			size: size,
			resolve: {}
		});
	};

	/* istanbul ignore next  */
	$scope.toggleAnimation = function () {
		$scope.animationsEnabled = !$scope.animationsEnabled;
	};

}

]);