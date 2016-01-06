app = angular.module('quotes.directives.qtForm', [
  'quotes.services.qtServices',
  'gallant.directives.glForm',
  'ui.bootstrap',
  'as.sortable',
]);

app.directive('qtQuoteForm', ['Quote', 'Service', 'Client', '$filter', function(Quote, Service, Client, $filter) {
    return {
        restrict: 'A',
        scope: {
          quote: '=',
          endpoint: '=',
          language: '=',
          forms: '=',
          boolTemplate : '=',
        },
    controller: ['$scope', '$attrs', '$filter', 'Quote', 'Service', 'QuoteTemplate', 'Client',
        function($scope, $attrs, $filter, Quote, Service, QuoteTemplate, Client) {
            $scope.isCollapsed = false;
            $scope.quoteFields = [];
            $scope.quoteStatus = [];
            $scope.quoteLanguage = [];
            $scope.serviceFields = [];
            $scope.language_list  = [];

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
                    description: "N/A",
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

            Client.query().$promise.then(function(clients) {
                $scope.clients = clients;
            });


            Quote.fields().$promise.then(function(fields) {
                for (var key in fields.status) {
                    // must create a temp object to set the key using a variable
                    var tempObj = {};
                    tempObj[key] = fields.status[key];
                    $scope.quoteStatus.push({
                        value: key,
                        text: tempObj[key]
                    });
                }

                for (var key in fields.language) {
                    // must create a temp object to set the key using a variable
                    var tempObj = {};
                    tempObj[key] = fields.language[key];
                    $scope.quoteLanguage.push({
                        value: key,
                        text: tempObj[key]
                    });
                }


            });

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

            if($attrs.boolTemplate != 'False'){
                console.log($attrs.boolTemplate);
                $scope.endpoint = QuoteTemplate;
            }else{
                $scope.endpoint = Quote;
            }

            if ($attrs.quoteId) {
                Quote.get({id: $attrs.quoteId}).$promise.then(function(quote) {
                    $scope.quote = quote;
                    if($attrs.language){
                        $scope.addLanguage($scope.language);
                    }
                });
            } else {
                if ($attrs.templateId) {
                    QuoteTemplate.get({
                        id: $attrs.templateId
                    }).$promise.then(function (quoteTemplate) {
                            $scope.quote = quoteTemplate.quote;
                            $scope.language_list = quoteTemplate.language_list;
                        });
                } else {
                    $scope.quote = {
                        "id": "",
                        "user": $attrs.userId,
                        "name": "New Quote",
                        "client": $attrs.clientId,
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
          }
        ],
        templateUrl: '/static/quotes/html/qt_quote_form.html',
        link: function($scope) {

            $scope.dynamicPopover = {
                templateUrl: 'myPopoverTemplate.html',
            };

            $scope.changeLanguage = function(lang){
                $scope.language = lang[0];
            }
            $scope.addLanguage = function(lang){
                selected = $filter('filter')($scope.quoteLanguage, {
                        value: lang,
                    }, true);
                if(selected){
                    $scope.language_list.push([selected[0].value,selected[0].text]);
                }
            }
            $scope.removeService = function(index) {
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
            }
            $scope.getTotal = function() {
                if ($scope.quote) {
                    if($scope.quote.services){
                        $scope.total = 0;
                        for (var i = 0; i < $scope.quote.services.length; i++) {
                            var service = $scope.quote.services[i];
                            if (service) {
                                $scope.total += (service.cost.amount * service.quantity);
                            } else {
                                $scope.total += 0;
                            }
                        }
                    }
                return $scope.total;
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