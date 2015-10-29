angular.module('gallant.services', [])
  .factory('gallantAPIservice', function($http) {

    var gallantAPI = {};

    /* GET Users */
    gallantAPI.getUsers = function() {
      var url = '/en/api/users/';
      return $http({
        method: 'GET', 
          url: url
      });
    }

    /* GET Tasks */
    gallantAPI.getTasks = function() {
      var url = '/en/calendar/api/tasks/';
      return $http({
        method: 'GET', 
          url: url
      });
    }

    /* POST Events */
    gallantAPI.postTask = function(data) {
      var url = '/en/calendar/api/task/add/';
      return $http({
        method: 'POST', 
          url: url,
          data: data,
      });
    }    

    return gallantAPI;
  });