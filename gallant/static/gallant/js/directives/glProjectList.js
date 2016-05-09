app = angular.module('gallant.directives.glProjectList', [
    'ui.bootstrap',
    'smart-table',
    'gallant.services.glServices',
    'gallant.directives.glAddModal',
    'gallant.directives.glProjectAdd',
]);

app.directive('glProjectList', ['$window', '$uibModal', 'Project', function ($window, $uibModal, Project) {
    return {
        restrict: 'A',
        scope: {
            projects: '=?',
        },
        controller: ['$scope', function ($scope) {
            if (!$scope.projects) {
                Project.query().$promise.then(function (response) {
                    $scope.projects = response;
                });
            }
        }],
        templateUrl: '/static/gallant/html/gl_project_list.html',
        link: function ($scope) {
            $scope.projectSaved = function (project) {
                $scope.projects.push(project);
                $scope.modalInstance.dismiss('cancel');
            };

            $scope.redirect = function (project) {
                $window.location.href = project.link;
            };

            $scope.checkAll = function () {
                angular.forEach($scope.projects, function (p) {
                    p.isSelected = $scope.selectedAll;
                });
            };
        }
    };
}]);