app = angular.module('gallant.directives.glPayments', [
    'gallant.services.glServices',
]);

app.directive('glPayments', ['Payment', function (Payment) {
    return {
        restrict: 'A',
        scope: {
            clientId: '@',
            openEditModal: '&',
        },
        controller: ['$scope', function ($scope) {}],
        templateUrl: '/static/gallant/html/gl_client_payments.html',
        link: function ($scope) {

            Payment.query({client_id: $scope.clientId}).$promise.then(function (response) {
                $scope.payments = response;
            });

        }
    };
}]);