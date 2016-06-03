var app = angular.module('glProjectDetail', [
    'ngResource',
    'ui.bootstrap',
    'gallant.controllers.glProjectDetailController',
    'gallant.controllers.glFormController',
    'gallant.directives.glAlerts',
    'gallant.directives.glAddModal',
    'gallant.directives.glProjectAdd',
]);

/* istanbul ignore next */
app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

/* istanbul ignore next */
app.config(["$resourceProvider",function ($resourceProvider) {
  // extend the default actions
  angular.extend($resourceProvider.defaults.actions,{
    // put your defaults here
    update : {
      method : "PATCH",
      isArray : false,
    }

  });
}]);