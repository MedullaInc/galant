var app = angular.module('qtQuoteList', [
    'ngResource',
    'ngAnimate',
    'smart-table',
    'ui.bootstrap',
    'quotes.controllers.qtQuoteListController',
    'quotes.controllers.qtQuoteTemplateListController',
    'quotes.controllers.qtPopoverController',
    'gallant.directives.glAlerts',
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