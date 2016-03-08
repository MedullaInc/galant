var app = angular.module('brief', [
    'ngResource',
    'xeditable',
    'briefs.directives.brDetail',
    'gallant.controllers.glFormController',
    'gallant.directives.glAlerts',
]);

/* istanbul ignore next */
app.config(function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

/* istanbul ignore next */
app.config(["$resourceProvider", function ($resourceProvider) {
    // extend the default actions
    angular.extend($resourceProvider.defaults.actions, {

        // put your defaults here
        update: {
            method: "PUT",
            isArray: false,
        }

    });
}]);

/* istanbul ignore next */
app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});