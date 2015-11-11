/**
 * calendarApp 
 */

angular.module('gallant', [
  'ui.calendar',
   'ui.bootstrap',
   'ng.django.forms',
   'ngResource',
   'gallant.directives',
   'gallant.controllers',
   'gallant.services',
   ])
.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $.cookie("csrftoken");
}]);

/* EOF */
