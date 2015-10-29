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

app.factory("Briefs", function ($resource) {
    return $resource("/en/briefs/api/brief/:id");
})