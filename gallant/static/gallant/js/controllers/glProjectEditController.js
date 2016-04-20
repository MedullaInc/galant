app = angular.module('gallant.controllers.glProjectEditController', []);

app.controller('glProjectEditController', ['$scope', '$uibModal',
    function ($scope, $uibModal) {

        $scope.addProject = function () {
            $scope.modalInstance = $uibModal.open({
                scope: $scope,
                animation: true,
                templateUrl: 'addProjectModal.html',
            });
            return 0;
        };

        $scope.projectSaved = function (project) {
            $scope.modalInstance.dismiss('cancel');
        };

        $scope.cancel = function () {
            $scope.modalInstance.dismiss('cancel');
        };
    }
]);