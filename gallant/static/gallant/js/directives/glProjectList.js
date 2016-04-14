app = angular.module('gallant.directives.glProjectList', [
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glProjectAdd',
]);

app.directive('glProjectList', ['$window', '$uibModal', 'Project', function ($window, $uibModal, Project) {
    return {
        restrict: 'A',
        scope: {
        },
        controller: ['$scope', function ($scope) {}],
        templateUrl: '/static/gallant/html/gl_project_list.html',
        link: function ($scope) {
            $scope.addProject = function() {
                $scope.modalInstance = $uibModal.open({
                    scope: $scope,
                    animation: true,
                    templateUrl: 'addProjectModal.html',
                });
                return 0;
            }
        }
    };
}]);