var app = angular.module('glUserDashboard', [
    'ngResource',
    'ui.bootstrap',
    'gallant.services.glServices',
    'gallant.directives.glDashboardWorkSummary',
    'gallant.directives.glDashboardMoneySummary',
    'gallant.controllers.glUserDashboardController',
    'gallant.directives.glAddModal',
    'tc.chartjs',
]);

/* istanbul ignore next */
app.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

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