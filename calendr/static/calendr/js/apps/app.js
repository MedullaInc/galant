/**
 * calendarApp
 */

var app = angular.module('gallant', [
        'ui.calendar',
        'ui.bootstrap',
        'ng.django.forms',
        'ngResource',
        'calendr.controllers.clCalendrController',
        'calendr.services.clServices',
        'gallant.services.glServices',
        'gallant.directives.glProjectList',
        'gallant.directives.glAlerts',
        'gallant.controllers.glFormController',
        'calendr.directives.clTaskList',
        'ui.bootstrap.tabs',
    ])
    .config(['$httpProvider', /* istanbul ignore next  */ function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

/* istanbul ignore next */
app.config(["$resourceProvider", function ($resourceProvider) {
    // extend the default actions
    angular.extend($resourceProvider.defaults.actions, {
        // put your defaults here
        update: {
            method: "PATCH",
            isArray: false,
        }
    });
}]);
