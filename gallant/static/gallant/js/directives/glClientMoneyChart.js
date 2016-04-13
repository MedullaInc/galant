app = angular.module('gallant.directives.glClientMoneyChart', [
    'gallant.services.glServices',
]);

app.directive('glClientMoneyChart', ['$window', 'Payment', function ($window, Payment) {
    return {
        restrict: 'A',
        scope: {
            clientId: '@',
        },
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_client_money_chart.html',
        link: function ($scope) {
            $scope.labels = ["Download Sales", "In-Store Sales", "Mail-Order Sales"];
            $scope.data = [300, 500, 100];
        }
    };
}]);