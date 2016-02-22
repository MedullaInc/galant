app = angular.module('quotes.controllers.qtPopoverController', ['ngAnimate','ui.bootstrap', 'quotes.services.qtServices']);

app.controller('qtPopoverController', ['$scope', '$http', '$window', '$rootScope', '$uibModal', 'Quote', 'QuoteTemplate',
    function($scope, $http, $window, $rootScope, $uibModal, Quote, QuoteTemplate) {

    $scope.quoteTemplates = $rootScope.quoteTemplates;

    $scope.init = function(addQuoteURL, currentLanguage) {
        $scope.addQuoteURL = addQuoteURL;
        $scope.currentLanguage = currentLanguage;
        $scope.selectedLanguage = currentLanguage;
    };

	$scope.dynamicPopover = {
		templateUrl: 'myPopoverTemplate.html',
	};

    $scope.redirectTemplate = function(quoteTemplate) {
        // In case there was no selection
        if(! quoteTemplate.languageSelection){
            quoteTemplate.languageSelection = $scope.currentLanguage;
        }       
        $window.location.href = $scope.addQuoteURL + "?template_id=" + quoteTemplate.id + "&lang=" + quoteTemplate.languageSelection;
    };

    $scope.addQuoteRedirect = function() {
        $window.location.href = $scope.addQuoteURL;
    };

    $scope.languageSelection = function(quoteTemplate, lang) {
        quoteTemplate.languageSelection = lang;
    };

	$scope.open = function () {
		$scope.modalInstance = $uibModal.open({
            scope: $scope,
			animation: true,
			templateUrl: 'myModalContent.html',
			controller: 'qtPopoverController',
		});
        return 0;
	};

}

]);