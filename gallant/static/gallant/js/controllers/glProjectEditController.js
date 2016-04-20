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

        $scope.redirect = function (project) {
            $window.location.href = project.link;
        };

        $scope.checkAll = function () {
            angular.forEach($scope.projectsSafe, function (p) {
                p.isSelected = $scope.selectedAll;
            });
        };

    }
]);