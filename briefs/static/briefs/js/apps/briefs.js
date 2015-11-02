var app = angular.module('brief', [
    'ngResource',
    'briefs.directives.brForm',
    'briefs.controllers.briefFormController',
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

app.factory("Brief", function ($resource) {
    // TODO: this shouldn't start with /en/
    return $resource("/en/briefs/api/brief/:id");
});

app.factory("BriefTemplate", function ($resource) {
    return $resource("/en/briefs/api/template/:id");
});

app.factory("Question", function ($resource) {
    return $resource("/en/briefs/api/question/:id");
});
