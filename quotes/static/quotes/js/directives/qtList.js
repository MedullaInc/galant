app = angular.module('quotes.directives.qtList', [
    'quotes.services.qtServices',
    'ui.bootstrap',
]);

app.directive('qtQuoteList', ['Quote', 'Service','$filter', function (Quote, Service, $filter) {
    return {
        restrict: 'A',
        scope: {
            quote: '=',
            endpoint: '=',
            language: '=',
            forms: '=',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote', 'Service', 'QuoteTemplate',
            function ($scope, $attrs, $filter, $window, Quote, Service, QuoteTemplate) {
                $scope.isCollapsed = true;
                $scope.quoteFields = [];
                $scope.serviceFields = [];

                $scope.endpoint = Quote;

                $scope.quoteDetail = function(quote) {
                    $window.location.href = '/en/quote/' + quote.id;
                };


                Service.fields({
                }).$promise.then(function (fields) {
                        for (var key in fields.type) {
                          // must create a temp object to set the key using a variable
                          var tempObj = {};
                          tempObj[key] = fields.type[key];
                          $scope.serviceFields.push({value: key, text: tempObj[key]});
                        }

                });

                Quote.all({
                }).$promise.then(function (quotes) {
                    $scope.quotes = quotes;
                });


            }],
        templateUrl: '/static/quotes/html/qt_quote_list.html',
          link: function($scope, $window) {


        }
    };
}]);
