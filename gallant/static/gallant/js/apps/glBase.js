var app = angular.module('glBase', [
    'ngResource',
    'gallant.directives.glAddModal',
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