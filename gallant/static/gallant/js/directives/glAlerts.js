app = angular.module('gallant.directives.glAlerts', ['gallant.services.glServices', 'ui.bootstrap', 'ngAnimate']);

app.directive('glAlerts', ['glAlertService', function (glAlertService) {
    return {
        restrict: 'A',
        template: '<uib-alert ng-repeat="alert in alerts.get()" type="{{alert.type}}"' +
                  'close="alerts.closeAlertIdx($index)" ng-hide="hideAlert($index)">{{alert.msg}}</uib-alert>',
        controller: function ($scope) {
            $scope.alerts = glAlertService;
        },
        link: function ($scope) {
        }
    };
}]);
