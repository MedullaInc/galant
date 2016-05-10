app = angular.module('kanban.services.kbServices', ['ngResource']);

/* istanbul ignore next  */
app.factory('KanbanCard', function ($resource) {
    return $resource('/en/kanban/api/card/:id');

});
