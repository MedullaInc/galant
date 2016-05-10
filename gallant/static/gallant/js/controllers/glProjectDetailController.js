app = angular.module('gallant.controllers.glProjectDetailController', ['gallant.services.glServices',
    'kanban.directives.kbBoardColumn']);

app.controller('glProjectDetailController', ['$scope', '$http', '$window', 'Service', 'glConstants',
    function ($scope, $http, $window, Service, glConstants) {
        $scope.glConstants = glConstants;

        $scope.init = function(serviceDetailURL, projectId) {
            $scope.serviceDetailURL = serviceDetailURL;
            Service.query({project_id: projectId}).$promise.then(function (services) {
                $scope.services = [];
                angular.forEach(services, function (s) {
                    s.name = s.name[s.language];
                    s.description = s.description[s.language];
                    $scope.services.push(s);
                });
            });
        };

        $scope.redirect = function(service) {
            $window.location.href = $scope.serviceDetailURL + service.id;
        };
    }
]);