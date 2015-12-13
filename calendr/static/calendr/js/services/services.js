app = angular.module('gallant.services', []);

app.factory('Project', function($resource) {
  return $resource('/en/api/projects');
});

app.factory('User', function($resource) {

  return $resource('/en/api/users');

});

app.factory('Task', function($resource) {
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