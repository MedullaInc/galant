/**
 * calendarApp
 */

angular.module('gallant', [
        'ui.calendar',
        'ui.bootstrap',
        'ng.django.forms',
        'ngResource',
        'calendr.controllers.clCalendrController',
        'gallant.services',
    ])
    .config(['$httpProvider', /* istanbul ignore next  */ function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = $.cookie("csrftoken");
    }]);

/* EOF */
