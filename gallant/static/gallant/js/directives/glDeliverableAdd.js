app = angular.module('gallant.directives.glDeliverableAdd', [
    'ui.bootstrap',
    'gallant.directives.glForm',
    'gallant.services.glServices',
]);

app.directive('glDeliverableAdd', ['$window', 'Service', 'Project', function ($window, Service, Project) {
    return {
        restrict: 'A',
        scope: {
            deliverable: '=?',
            project: '=?',
            language: '@',
            onSuccess: '&',
            onDeleted: '&',
        },
        controller: ['$scope', function ($scope) {

            if (!$scope.deliverable) {
                $scope.deliverable = new Service();
                if ($scope.project) {
                    $scope.deliverable.project = $scope.project.id;
                }
            }

            $scope.objectEndpoint = Project;
            $scope.object = $scope.project;

            $scope.saveDeliverable = function() {
                $scope.project.services.push($scope.deliverable);
            };

            $scope.deleteDeliverable = function() {
                var idx = $scope.project.services.findIndex(function (e) { return $scope.deliverable.id == e.id; });
                $scope.project.services.splice(idx, 1);
            };

            $scope.projectSaved = $scope.onSuccess();

        }],
        templateUrl: '/static/gallant/html/gl_deliverable_add.html',
        link: function ($scope) {
        }
    };
}]);