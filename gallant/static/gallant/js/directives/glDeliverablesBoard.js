app = angular.module('gallant.directives.glDeliverablesBoard', [
    'gallant.services.glServices',
    'kanban.directives.kbBoardColumn',
]);

app.directive('glDeliverablesBoard', ['Project', 'Service', function (Project, Service) {
    return {
        restrict: 'A',
        scope: {
        },
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_service_board.html',
        link: function ($scope) {
            $scope.services = [];
            Project.query().$promise.then(function (response) {
                angular.forEach(response, function (p) {
                    Service.query({project_id: p.id}).$promise.then(function (services) {
                        angular.forEach(services, function (s) {
                            $scope.services.push(s);
                        });
                    });
                });
            });
        }
    };
}]);