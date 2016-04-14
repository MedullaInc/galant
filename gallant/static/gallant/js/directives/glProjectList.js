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
        controller: ['$scope', function ($scope) {
            $scope.projects = [
                {name: 'Project 1', client: 'Kanye West', status: 0, field_choices: {status: ['Assigned']}},
                {name: 'Tight Logo', client: 'Lil Wayne', status: 0, field_choices: {status: ['Assigned']}},
                {name: 'Company Branding', client: 'Wes Anderson', status: 0, field_choices: {status: ['Assigned']}},
            ];
        }],
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

            $scope.cancel = function () {
                $scope.modalInstance.dismiss('cancel');
            }
        }
    };
}]);