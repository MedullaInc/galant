var app = angular.module('glClientPayments', [
    'ngResource',
    'ui.bootstrap',
    'ng.django.forms',
    'gallant.services.glServices',
    'gallant.controllers.glClientPaymentController',
    'quotes.controllers.qtPopoverController',
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