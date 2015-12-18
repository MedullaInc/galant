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
    ])
    .config(['$httpProvider', /* istanbul ignore next  */ function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = $.cookie("csrftoken");
    }]);

/* EOF */
