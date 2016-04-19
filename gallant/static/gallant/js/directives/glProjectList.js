app = angular.module('gallant.directives.glProjectList', [
    'ui.bootstrap',
    'smart-table',
    'gallant.services.glServices',
    'gallant.directives.glProjectAdd',
]);

app.directive('glProjectList', ['$window', '$uibModal', 'Project', function ($window, $uibModal, Project) {
    return {
        restrict: 'A',
        scope: {
        },
        controller: ['$scope', function ($scope) {
            Project.query().$promise.then(function (response) {
                $scope.projectsSafe = response;
            });
        }],
        templateUrl: '/static/gallant/html/gl_project_list.html',
        link: function ($scope) {
            $scope.addProject = function () {
                $scope.modalInstance = $uibModal.open({
                    scope: $scope,
                    animation: true,
                    templateUrl: 'addProjectModal.html',
                });
                return 0;
            };

            $scope.projectSaved = function (project) {
                $scope.projectsSafe.push(project);
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
    };
}]);