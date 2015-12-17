app = angular.module('quotes.directives.qtForm', [
  'quotes.services.qtServices',
  'gallant.directives.glForm',
  'ui.bootstrap',
  'as.sortable',
]);

app.directive('qtQuoteForm', ['Quote', 'Service', '$filter', function(Quote, Service, $filter) {
  return {
    restrict: 'A',
    scope: {
      quote: '=',
      endpoint: '=',
      language: '=',
      forms: '=',
    },
    controller: ['$scope', '$attrs', '$filter', '$location', 'Quote', 'Service', 'QuoteTemplate',
      function($scope, $attrs, $filter, $location, Quote, Service, QuoteTemplate) {
        $scope.isCollapsed = true;
        $scope.quoteFields = [];
        $scope.serviceFields = [];

        $scope.endpoint = Quote;

        $scope.location = $location.search();

        $scope.addSection = function(section_name) {
          var name = "";
          if (section_name) {
            name = section_name;
          } else {
            var counter = $scope.quote.sections.length;
            name = "section_" + (counter++);
          }
          $scope.inserted = {
            title: "",
            text: "",
            name: name,
            index: counter,
          }

          $scope.quote.sections.push($scope.inserted);
        };

        $scope.addService = function() {
          $scope.inserted = {
            cost: {
              amount: "0",
              currency: "USD",
            },
            description: "Some service",
            user: 1,
            name: "",
            notes: Array[0],
            parent: null,
            quantity: "",
            type: "",
            user: "1",
          };
          $scope.quote.services.push($scope.inserted);
        };

        Service.fields({}).$promise.then(function(fields) {
          for (var key in fields.type) {
            // must create a temp object to set the key using a variable
            var tempObj = {};
            tempObj[key] = fields.type[key];
            $scope.serviceFields.push({
              value: key,
              text: tempObj[key]
            });
          }

        });
        if ($attrs.quoteId) {
          console.log($attrs);
          Quote.get({
            id: $attrs.quoteId
          }).$promise.then(function(quote) {
            $scope.quote = quote;
          });
        } else {

          if ($attrs.quoteTemplateId) {
            

          } else {
          $scope.quote = {
            "id": "",
            "user": "",
            "name": "New Quote",
            "client": "1",
            "sections": [],
            "services": [],
            "status": "0",
            "modified": "",
            "token": "",
            "parent": null,
            "projects": []
          }
          $scope.addSection('intro');
          $scope.addSection('important_notes');
          $scope.addService();
        }

      }
    }],
    templateUrl: '/static/quotes/html/qt_quote_form.html',
    link: function($scope) {



      $scope.removeServiceSection = function(index) {
        $scope.quote.services.splice(index, 1);
      };

      $scope.showType = function(service) {

        if (service) {
          var selected = [];
          selected = $filter('filter')($scope.serviceFields, {
            value: service.type
          });
          return selected.length ? selected[0].text : 'Not set';
        }
      };

      $scope.getTotal = function() {
        if ($scope.quote) {
          var total = 0;
          for (var i = 0; i < $scope.quote.services.length; i++) {
            var service = $scope.quote.services[i];
            if (service) {
              total += (service.cost.amount * service.quantity);
            } else {
              total += 0;
            }
          }
          return total;
        }
      }


      $scope.removeSection = function(index) {
        $scope.quote.sections.splice(index, 1);
      };


      $scope.dragControlListeners = {
        orderChanged: function(event) {

        },
      };


    }
  };
}]);