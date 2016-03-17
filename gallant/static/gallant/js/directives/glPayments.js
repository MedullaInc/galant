app = angular.module('galant.directives.glPayments', [
    'gallant.services.glServices',
]);

app.directive('glPayments', ['Payments', function (Payments) {
    return {
        restrict: 'A',
        scope: true,
        controller: ['$scope', function ($scope) {}],
        templateUrl: '/static/galant/html/gl_client_payments.html',
        link: function ($scope) {

            Payment.query({client_id: $attrs.clientId}).$promise.then(function (response) {
                $scope.payments = response;
            });

        }
    };
}]);