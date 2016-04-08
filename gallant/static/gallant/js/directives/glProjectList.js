app = angular.module('gallant.directives.glProjectList', [
    'gallant.services.glServices',
]);

app.directive('glProjectList', ['$window', 'Project', function ($window, Project) {
    return {
        restrict: 'A',
        scope: {
        },
        controller: ['$scope', function ($scope) {}],
        templateUrl: '/static/gallant/html/gl_project_list.html',
        link: function ($scope) {
        }
    };
}]);