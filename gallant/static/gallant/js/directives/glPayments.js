app = angular.module('gallant.directives.glPayments', [
    'gallant.services.glServices',
]);

app.directive('glPayments', ['Payment', function (Payment) {
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
        }
    };
}]);