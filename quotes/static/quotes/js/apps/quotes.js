var app = angular.module('quote', [
    'ngResource',
    'gallant.controllers.glFormController',
    'quotes.controllers.qtPopoverController',
    'quotes.directives.qtForm',
    'quotes.directives.qtList',
    'quotes.directives.qtTemplateList',
    'ui.bootstrap',
    'ngAnimate',
    'xeditable'
]);

app.config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

app.config(["$resourceProvider",function ($resourceProvider) {
  // extend the default actions
  angular.extend($resourceProvider.defaults.actions,{


    // put your defaults here
    update : {
      method : "PUT",
      isArray : false,
    }

  });
}]);