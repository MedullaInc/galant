app = angular.module('gallant.services.glServices', ['ngResource']);

/* istanbul ignore next */
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
            url: '/api/client/:id'
        },
        fields: {
            method: 'GET',
            url: '/api/client/fields'
        },
        // the following are untested
        save: {
            method: 'POST',
            params: {
                client: '@client'
            },
        },
        update: {
            method: 'PATCH',
            params: {
                id: '@id'
            },
            url: '/api/client/:id'
        },
        replace: {
            method: 'PUT',
            params: {
                id: '@id'
            },
            url: '/api/client/:id'
        }
    });

});

/* istanbul ignore next */
app.factory('PaymentAPI', function ($resource) {
    return $resource('/en/quote/api/payment/:id');
});

/* istanbul ignore next  */
app.factory('Project', function ($resource) {
    return $resource('/en/api/projects');
});

/* istanbul ignore next  */
app.factory('ClientProjects', function ($resource) {
    return $resource('/en/api/projects?client_id=:id', {id: '@id'});
});

///* istanbul ignore next  */
//app.factory('ClientQuoteDetail', function ($resource) {
//    return $resource('/en/quote/api/payments/:client_id/:id', {client_id: '@client_id', id: '@id'});
//});

/* istanbul ignore next  */
app.factory('User', function ($resource) {
    return $resource('/en/api/users');
});

app.factory('glValidate', function () {
    return {
        nonEmpty: function ($data) {
            if (!$data || $data == "") {
                return "This field cannot be empty.";
            }
        },

        selected: function ($data) {
            if (!$data || $data == "") {
                return "You must choose a value.";
            }
        },

        selectedIf: function ($data, condition) {
            if (condition && (!$data || $data == "")) {
                return "You must choose a value.";
            }
        },
    };
});