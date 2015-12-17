app = angular.module('quotes.directives.qtTemplateList', [
    'quotes.services.qtServices',
]);

app.directive('qtQuoteTemplateList', ['Quote', 'QuoteTemplate', 'Service', 'Client', '$filter', function (Quote, QuoteTemplate, Service, Client, $filter) {
    return {
        restrict: 'A',
        scope: {
            quote: '=',
            endpoint: '=',
            language: '=',
            forms: '=',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote', 'QuoteTemplate', 'Service', 'Client',
            function ($scope, $attrs, $filter, $window, Quote, QuoteTemplate, Service, Client) {
                $scope.isCollapsed = true;
                $scope.quoteStatus = [];
                $scope.selectedItem = "";

                $scope.endpoint = Quote;

                $scope.goToUrl = function(template) {
                    $window.location.href = '/en/quote/add/' + '?template_id=' + template.id + '&lang=' + template.languageSelection;
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
                    console.log($scope.quotes);
                });

                QuoteTemplate.all({
                }).$promise.then(function (quoteTemplates) {
                    $scope.quoteTemplates = quoteTemplates;
                });

            }],
        templateUrl: '/static/quotes/html/qt_quote_template_list.html',
          link: function($scope, $window) {

          $scope.languageSelection = function(template, lang) {
			template.languageSelection = lang;             	

          };

        }
    };
}]);
