app = angular.module('gallant.controllers.glUserDashboardController', [
    'gallant.directives.glAddModal']);

app.controller('glUserDashboardController', ['$scope',
    function ($scope) {
        $scope.$watch('openOnboarding', function (oldVal, newVal) {
            $scope.openOnboarding();
        });
    }
]);