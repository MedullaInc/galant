app = angular.module('gallant.services.glServices', ['ngResource']);

app.factory('Client', function ($resource) {
    return $resource('/api/client', {}, {
        query: {
            method: 'GET',
            params: {},
            isArray: true
        },
        retrieve: {
            method: 'GET',
            params: {},
            isArray: true,
            url: '/api/client/:id '
        },
        // the following are untested
        save: {
            method: 'POST',
            params: {
                client: '@client'
            },
        },
        update: {
            method: 'PUT',
            params: {
                id: '@id'
            },
            url: '/api/client/:id '
        }
    });

});
