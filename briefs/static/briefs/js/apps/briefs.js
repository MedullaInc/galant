var app = angular.module('brief', [
    'briefs.directives.brQuestionForm',
    'briefs.directives.brBriefForm',
    'briefs.directives.brUltextInput',
    'briefs.controllers.briefFormController',
]);

app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});