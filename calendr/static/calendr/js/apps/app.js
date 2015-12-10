/**
 * calendarApp
 */

angular.module('gallant', [
        'ui.calendar',
        'ui.bootstrap',
        'ng.django.forms',
        'ngResource',
        'calendr.controllers.clCalendrController',
        'calendr.services.clServices',
        'gallant.services.glServices',
    ])
    .config(['$httpProvider', /* istanbul ignore next  */ function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = $.cookie("csrftoken");
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);

/* EOF */
