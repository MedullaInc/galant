app = angular.module('gallant.directives.glDeliverablesBoard', [
    'gallant.services.glServices',
    'kanban.directives.kbBoardColumn',
]);

app.directive('glDeliverablesBoard', ['Service', 'glConstants', '$http', '$window', function (Service, glConstants, $http, $window) {
    return {
        restrict: 'A',
        scope: {},
        controller: ['$scope', '$http', '$window', function ($scope, $http, $window) {
            $scope.glConstants = glConstants;
        }],
        templateUrl: '/static/gallant/html/gl_service_board.html',
        link: function ($scope) {
            Service.query({project_open: true}).$promise.then(function (services) {
                $scope.services = services;
            });

            $scope.redirect = function (service) {
                $window.location.href = service.card.link;
            };

        }
    };
}]);