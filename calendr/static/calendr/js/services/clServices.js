app = angular.module('calendr.services.clServices', ['ngResource']);

/* istanbul ignore next  */
app.factory('Task', function ($resource) {
    return $resource('/en/projects/api/task/:id');

});

/* istanbul ignore next  */
app.factory('FC', function () {
    return $.fullCalendar;
});
/* istanbul ignore next  */
app.factory('moment', function () {
    return moment;
});