angular.module('gallant.services', [])
  .factory('gallantAPIservice', function($http) {

    var gallantAPI = {};



    /* GET Users */
    gallantAPI.getProjects = function() {
      var url = '/en/api/projects/';
      return $http({
        method: 'GET', 
          url: url
      });
    }

    /* GET Users */
    gallantAPI.getUsers = function(project) {      
      if(project){
       var url = '/en/api/users/?project_id='+project.id;
      }else{
       var url = '/en/api/users/';
      }
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

    /* UPDATE Task */
    gallantAPI.updateTask = function(data) {

      var url = '/en/calendar/api/task/'+data.id;
      console.log(data);
      return $http({
        method: 'PUT', 
          url: url,
          data: data,
      });
    }

    /* POST Tasks */
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