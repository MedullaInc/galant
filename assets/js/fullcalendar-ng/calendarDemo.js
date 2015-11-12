/**
 * calendarDemoApp - 0.9.0
 */
angular.module('gallant', [
  'ui.calendar',
   'ui.bootstrap',
   'ng.django.forms',
   'gallant.controllers',
   'gallant.services',
   ])
.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = '{{ csrf_token|escapejs }}';
}]);


/* EOF */
