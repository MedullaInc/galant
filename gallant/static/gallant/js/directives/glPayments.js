app = angular.module('gallant.directives.glPayments', [
    'gallant.services.glServices',
]);

app.directive('glPayments', ['$window','Payment', function ($window,Payment) {
    return {
        restrict: 'A',
        scope: {
            clientId: '@',
            openEditModal: '&',
            payments: '=?'
        },
        controller: ['$scope', function ($scope) {}],
        templateUrl: '/static/gallant/html/gl_client_payments.html',
        link: function ($scope) {

            $scope.deletePayment = function(payment) {
                if ($window.confirm('Are you sure?')) {
                    Payment.delete({id: payment.id});
                    $scope.payments.splice($scope.payments.indexOf(payment),1);
                }
            }

        }
    };
}]);