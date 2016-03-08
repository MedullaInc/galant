app = angular.module('gallant.directives.glAlerts', ['gallant.services.glServices', 'ui.bootstrap']);

app.directive('glAlerts', ['glAlertService', function (glAlertService) {
    return {
        restrict: 'A',
        template: '<uib-alert ng-repeat="alert in alerts" type="{{alert.type}}" close="closeAlert($index)">{{alert.msg}}</uib-alert>',
        controller: function($scope) {
            $scope.alerts = glAlertService.get();
        },
    };
}]);
