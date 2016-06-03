app = angular.module('gallant.controllers.glProjectDetailController', ['gallant.services.glServices',
    'kanban.directives.kbBoardColumn']);

app.controller('glProjectDetailController', ['$scope', '$http', '$window', 'Project', 'glConstants',
    function ($scope, $http, $window, Project, glConstants) {
        $scope.glConstants = glConstants;

        $scope.init = function(serviceDetailURL, projectId) {
            $scope.serviceDetailURL = serviceDetailURL;
            Project.get({id: projectId}).$promise.then(function (project) {
                $scope.project = project;
                $scope.services = $scope.project.services;
            });
        };

        $scope.redirect = function(service) {
            $window.location.href = $scope.serviceDetailURL + service.id;
        };

        $scope.projectSaved = function (project) {
            $scope.project = project;
            $scope.services = $scope.project.services;

            $scope.modalInstance.dismiss('cancel');
        };
    }
]);