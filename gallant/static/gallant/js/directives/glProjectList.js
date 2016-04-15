app = angular.module('gallant.directives.glProjectList', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glProjectAdd',
]);

app.directive('glProjectList', ['$window', '$uibModal', 'Project', function ($window, $uibModal, Project) {
    return {
        restrict: 'A',
        scope: {
            redirectUrl: '@',
        },
        controller: ['$scope', function ($scope) {
            Project.query().$promise.then(function (response) {
                $scope.projects = response;
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
            }

            $scope.projectSaved = function (project) {
                $scope.projects.push(project);
                $scope.modalInstance.dismiss('cancel');
            }

            $scope.cancel = function () {
                $scope.modalInstance.dismiss('cancel');
            }

            $scope.redirect = function(id) {
                $window.location.href = $scope.redirectUrl + id;
            };
        }
    };
}]);