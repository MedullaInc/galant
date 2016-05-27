app = angular.module('calendr.services.clServices', ['ngResource']);

/* istanbul ignore next  */
app.factory('Task', ['$resource', function ($resource) {
    return $resource('/en/projects/api/task/:id', {}, {
        update: {
          method: 'PATCH',
        }
    });

}]);

/* istanbul ignore next  */
app.factory('FC', function () {
    return $.fullCalendar;
});
/* istanbul ignore next  */
app.factory('moment', function () {
    return moment;
});

app.factory('clConstants', function () {
    return {
        TaskStatus: {
            ToDo: 0,
            Ready: 1,
            InProgress: 2,
            Done: 3,
        },
    };
});