app = angular.module('calendr.services.clServices', ['ngResource']);

/* istanbul ignore next  */
app.factory('Project', function ($resource) {
    return $resource('/en/api/projects');
});

/* istanbul ignore next  */
app.factory('User', function ($resource) {

    return $resource('/en/api/users');

});

/* istanbul ignore next  */
app.factory('Task', function ($resource) {
    return $resource('/en/calendar/api/task ', {}, {
        query: {
            method: 'GET',
            params: {},
            isArray: true
        },
        save: {
            method: 'POST',
            params: {
                task: '@task'
            },
        },
        update: {
            method: 'PUT',
            params: {
                id: '@id'
            },
            url: '/en/calendar/api/task/:id '
        },
        delete: {
            method: 'DELETE',
            params: {
                id: '@id'
            },
            url: '/en/calendar/api/task/:id '
        }
    });

});

/* istanbul ignore next  */
app.factory('FC', function () {
    return $.fullCalendar;
});
/* istanbul ignore next  */
app.factory('moment', function () {
    return moment;
});