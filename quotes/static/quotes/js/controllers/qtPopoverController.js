app = angular.module('quotes.controllers.qtPopoverController', ['ngAnimate', 'ui.bootstrap']);

app.controller('qtPopoverController', function ($scope, $uibModal, $log, $window) {

	$scope.dynamicPopover = {
		templateUrl: 'myPopoverTemplate.html',
	};

	$scope.goToUrl = function(url) {
	  $window.location.href = url;
	};
	

	$scope.animationsEnabled = true;

	$scope.open = function (size) {

	var modalInstance = $uibModal.open({
	  animation: $scope.animationsEnabled,
	  templateUrl: 'myModalContent.html',
	  controller: 'qtPopoverController',
	  size: size,
	  resolve: {
	    items: function () {
	      return $scope.items;
	    }
	  }
	});

	modalInstance.result.then(function (selectedItem) {
	  $scope.selected = selectedItem;
	}, function () {
	  $log.info('Modal dismissed at: ' + new Date());
	});
	};

	$scope.toggleAnimation = function () {
	$scope.animationsEnabled = !$scope.animationsEnabled;
	};

	$scope.items = ['item1', 'item2', 'item3'];

	$scope.items = ['item1', 'item2', 'item3'];
	$scope.selected = {
	item: $scope.items[0]
	};

	$scope.ok = function () {
	$uibModalInstance.close($scope.selected.item);
	};

	$scope.cancel = function () {
	$uibModalInstance.dismiss('cancel');
	};

});