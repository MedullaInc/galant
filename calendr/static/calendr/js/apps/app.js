/**
 * calendarApp
 */

var app = angular.module('gallant', [
  'ui.calendar',
   'ui.bootstrap',
   'ng.django.forms',
   'ngResource',
   'gallant.directives',
   'gallant.controllers',
   'gallant.services',
   ])
/* istanbul ignore next */
app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

}]);


/* EOF */
