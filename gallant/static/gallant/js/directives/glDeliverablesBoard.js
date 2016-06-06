app = angular.module('gallant.directives.glDeliverablesBoard', [
    'gallant.services.glServices',
    'kanban.directives.kbBoardColumn',
]);

app.directive('glDeliverablesBoard', ['Project', 'Service', 'glConstants', function (Project, Service, glConstants) {
    return {
        restrict: 'A',
        scope: {
        },
        controller: ['$scope', function ($scope) {
            $scope.glConstants = glConstants;
        }],
        templateUrl: '/static/gallant/html/gl_service_board.html',
        link: function ($scope) {
            $scope.services = [];
            Service.query({project_open: true}).$promise.then(function (services) {
                $scope.services = services;
            });
        }
    };
}]);