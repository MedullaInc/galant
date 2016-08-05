app = angular.module('gallant.controllers.glProjectDetailController', ['gallant.services.glServices',
    'kanban.directives.kbBoardColumn',
    'gallant.directives.glDeliverableAdd',
]);

app.controller('glProjectDetailController', ['$scope', '$http', '$window', 'Project', 'glConstants',
    function ($scope, $http, $window, Project, glConstants) {
        $scope.glConstants = glConstants;

        $scope.init = function (serviceDetailURL, projectId, language) {
            $scope.serviceDetailURL = serviceDetailURL;
            $scope.language = language;
            Project.get({id: projectId}).$promise.then(function (project) {
                $scope.project = project;
                $scope.services = project.services;
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