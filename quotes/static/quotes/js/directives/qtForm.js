app = angular.module('quotes.directives.qtForm', [
    'quotes.services.qtServices',
    'gallant.directives.glForm',
    'ui.bootstrap',
    'as.sortable',
]);

app.directive('qtQuoteForm', ['Quote', 'Service','$filter', function (Quote, Service, $filter) {
    return {
        restrict: 'A',
        scope: {
            quote: '=',
            endpoint: '=',
            language: '=',
            forms: '=',
        },
        controller: ['$scope', '$attrs', '$filter', 'Quote', 'Service', 'QuoteTemplate',
            function ($scope, $attrs, $filter, Quote, Service, QuoteTemplate) {

                $scope.isCollapsed = true;
                $scope.quoteFields = [];
                $scope.serviceFields = [];

                $scope.endpoint = Quote;
                if ($attrs.quoteId) {
                    Quote.get({
                        id: $attrs.quoteId
                    }).$promise.then(function (quote) {
                            $scope.quote = quote;
                        });
                    Service.fields({
                    }).$promise.then(function (fields) {
                            for (var key in fields.type) {
                              // must create a temp object to set the key using a variable
                              var tempObj = {};
                              tempObj[key] = fields.type[key];
                              $scope.serviceFields.push({value: key, text: tempObj[key]});
                            }

                    });
                } else {
                	// TO-DO TEMPLATES
                    // }
                }
            }],
        templateUrl: '/static/quotes/html/qt_quote_form.html',
          link: function($scope) {
              $scope.addService = function() {
                  $scope.inserted = {
                      cost: {
                          amount: "0",
                          currency: "AFN",
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

              $scope.removeServiceSection = function(index) {
                  $scope.quote.services.splice(index, 1);
              };

              $scope.showType = function(service) {

                if(service) {
                  var selected = [];
                  selected = $filter('filter')($scope.serviceFields, {value: service.type});
                  return selected.length ? selected[0].text : 'Not set';
                  }
              };

              $scope.getTotal = function(){
                  if($scope.quote){
                    var total = 0;
                    for(var i = 0; i < $scope.quote.services.length; i++){
                        var service = $scope.quote.services[i];
                        if(service){
                          total += (service.cost.amount * service.quantity);
                        }else{
                          total += 0;
                        }
                    }
                    return total;
                  }
              }

              $scope.addSection = function() {
                var counter = $scope.quote.sections.length;
                $scope.inserted = {
                  title: "",
                  text: "",
                  name: "section_"+(counter++),
                  index: counter,
              }
                $scope.quote.sections.push($scope.inserted);
              };              

              $scope.removeSection = function(index) {
                  $scope.quote.sections.splice(index, 1);
              };


              $scope.dragControlListeners = {
              	/*
                  accept: function (sourceItemHandleScope, destSortableScope) {return boolean},//override to determine drag is allowed or not. default is true.
                  itemMoved: function (event) {},//Do what you want},
                */
                  orderChanged: function(event) {

                  },//Do what you want},
              };
        }
    };
}]);
