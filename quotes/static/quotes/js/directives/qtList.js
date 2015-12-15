app = angular.module('quotes.directives.qtList', [
    'quotes.services.qtServices',
    'ui.bootstrap',
]);

app.directive('qtQuoteList', ['Quote', 'Service', 'Client', '$filter', function (Quote, Service, Client, $filter) {
    return {
        restrict: 'A',
        scope: {
            quote: '=',
            endpoint: '=',
            language: '=',
            forms: '=',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote', 'Service', 'Client', 'QuoteTemplate',
            function ($scope, $attrs, $filter, $window, Quote, Service, Client, QuoteTemplate) {
                $scope.isCollapsed = true;
                $scope.quoteStatus = [];

                $scope.endpoint = Quote;

                $scope.quoteDetail = function(quote) {
                    $window.location.href = '/en/quote/' + quote.id;
                };

                Quote.fields({
                }).$promise.then(function (fields) {
                        for (var key in fields.status) {
                          // must create a temp object to set the key using a variable
                          var tempObj = {};
                          tempObj[key] = fields.status[key];
                          $scope.quoteStatus.push({value: key, text: tempObj[key]});
                        }
                });

                Quote.all({
                }).$promise.then(function (quotes) {
                    $scope.quotes = quotes;
                });

                Client.all({
                }).$promise.then(function (clients) {
                    $scope.clients = clients;
                });

            }],
        templateUrl: '/static/quotes/html/qt_quote_list.html',
          link: function($scope, $window) {

              $scope.getQuoteStatus = function(quote) {
                if(quote) {
                  var selected = [];
                  selected = $filter('filter')($scope.quoteStatus, {value: quote.status});
                  return selected.length ? selected[0].text : 'Not set';
                  }
              };

              $scope.getQuoteClient = function(quote) {
                if(quote) {
                  var selected = [];
                  selected = $filter('filter')($scope.clients, {id: quote.client});
                  return selected.length ? selected[0].name : 'Not set';
                  }
              };

        }
    };
}]);
