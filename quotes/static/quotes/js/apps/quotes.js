var app = angular.module('quote', [
    'ngResource',
    'ngAnimate',
    'smart-table',
    'ui.bootstrap',
    'xeditable',
    'gallant.controllers.glFormController',
    'quotes.controllers.qtPopoverController',
    'quotes.controllers.qtQuoteTemplateListController',
    'quotes.directives.qtForm',
    'quotes.directives.qtClientForm',
    'gallant.directives.glAlerts',
    'gallant.directives.glProjectAdd',
    'gallant.directives.glAddModal',
]);

/* istanbul ignore next */
app.run(function(editableOptions) {
  editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
});

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
            method: "PATCH",
            isArray: false,
        }

    });
}]);