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
        'gallant.controllers.glFormController',
        'calendr.directives.clTaskList',
        'ui.bootstrap.tabs',
    ])
    .config(['$httpProvider', /* istanbul ignore next  */ function ($httpProvider) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = $.cookie("csrftoken");
    }]);

/* EOF */