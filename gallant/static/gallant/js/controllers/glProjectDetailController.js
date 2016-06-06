app = angular.module('gallant.controllers.glProjectDetailController', ['gallant.services.glServices',
    'kanban.directives.kbBoardColumn']);

app.controller('glProjectDetailController', ['$scope', '$http', '$window', 'Project', 'Service', 'glConstants',
    function ($scope, $http, $window, Project, Service, glConstants) {
        $scope.glConstants = glConstants;

        $scope.init = function (serviceDetailURL, projectId) {
            $scope.serviceDetailURL = serviceDetailURL;
            Project.get({id: projectId}).$promise.then(function (project) {
                $scope.project = project;
            });
            Service.query({project_id: projectId}).$promise.then(function (services) {
                $scope.services = services;
            });
        };

        $scope.redirect = function (service) {
            $window.location.href = $scope.serviceDetailURL + service.id;
        };
        
        $scope.editProjectSafe = function () {
            $scope.projectSafe = angular.copy($scope.project);
            $scope.editProject();
        };

        $scope.projectSaved = function (project) {
            $scope.modalInstance.dismiss('cancel');
            $window.location.reload();
        };
    }
]);