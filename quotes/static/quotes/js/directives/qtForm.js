app = angular.module('quotes.directives.qtForm', [
    'quotes.services.qtServices',
    'quotes.filters.qtCutFilter',
    'quotes.directives.qtServiceTable',
    'quotes.directives.qtSectionTable',
    'gallant.directives.glForm',
    'ui.bootstrap',
    'as.sortable']);

app.directive('qtQuoteForm', ['Quote', 'Service', 'Section', 'Client', '$filter', '$uibModal', function (Quote, Service, Section, Client, $filter, $uibModal) {
    return {
        restrict: 'A',
        scope: {
            quote: '=',
            quoteTemplate: '=',
            endpoint: '=',
            language: '=',
            forms: '=',
            boolTemplate: '=',
            idType: '=',
        },
        controller: ['$scope', '$attrs', '$filter', '$window', 'Quote', 'Service', 'Section', 'QuoteTemplate', 'Client',
            function ($scope, $attrs, $filter, $window, Quote, Service, Section, QuoteTemplate, Client) {
                $scope.quoteFields   = [];
                $scope.quoteStatus   = {};
                $scope.quoteLanguage = {};
                $scope.language_list = {};
                $scope.newQuote      = false;

                $scope.idType = $attrs.idType;
                $scope.boolTemplate = $attrs.boolTemplate;

                if($attrs.idType == "token"){
                    $window.onbeforeunload  = function () { 
                        $scope.quote.session_duration = ((new Date() - $scope.$parent.startTime)/1000 );
                        $scope.quote.views  = $scope.quote.views+1;
                        $scope.quote.status = "3";
                        Quote.update({id: $scope.quote.id}, $scope.quote);
                    }
                }

                Client.get().$promise.then(function (clients) {
                    $scope.clients = clients;
                });

                Quote.fields().$promise.then(function (fields) {
                    $scope.quoteStatus   = fields.status;
                    $scope.quoteLanguage = fields.language;
                });

            $scope.addSection = function (section_name) {
                var name = "";
                var counter;

                if (section_name) {
                    name = section_name;
                } else {
                    counter = $scope.quote.sections.length;
                    name = "section_" + (counter++);
                }
                $scope.section       = new Section({"name":name, "index":counter, "text":{}, "title":{}, "views":0});
                $scope.quote.sections.push($scope.section);
            };

            $scope.addService = function (service) {
                if (service) {
                    $scope.service = service;
                    $scope.modalInstance.close();
                } else {
                    $scope.service              = new Service();
                    $scope.service.name         = {}
                    $scope.service.description  = {}
                    $scope.service.user         = $scope.quote.user;
                    $scope.service.cost         = {amount:0, currency:"USD"}
                }
                $scope.service.user = $scope.quote.user;
                $scope.quote.services.push($scope.service);
            };
                

                if ($attrs.boolTemplate == "False") {
                    $scope.endpoint = Quote;
                } else {
                    $scope.endpoint = QuoteTemplate;
                }

                if ($attrs.quoteId) {
                    Quote.get({id: $attrs.quoteId}).$promise.then(function (quote) {
                        $scope.quote = quote;
                        if ($scope.language) {
                            $scope.language_list[$scope.language] = $scope.quoteLanguage[$scope.language];
                        }

                        if ($attrs.boolTemplate == "True") {
                            $scope.quoteTemplate = {
                                "quote": $scope.quote
                            };
                            $scope.quoteTemplate.quote.id = null;
                        }

                    });
                } else if ($attrs.templateId) {
                        QuoteTemplate.get({
                            id: $attrs.templateId
                        }).$promise.then(function (quoteTemplate) {
                            $scope.quote = quoteTemplate.quote;
                            $scope.quoteTemplate = quoteTemplate;
                            $scope.language_list = quoteTemplate.language_list;

                            if ($attrs.boolTemplate != "True") {
                                $scope.quote.id = null;
                            }
                        });
                    } else {
                        $scope.quote                    = new Quote();
                        $scope.quote.user               = $attrs.userId;
                        $scope.quote.client             = $attrs.clientId;
                        $scope.quote.projects           = [];
                        $scope.quote.services           = [];
                        $scope.quote.sections           = [];
                        $scope.quote.views              = 0;
                        $scope.quote.session_duration   = 0.0;

                        $scope.quoteTemplate            = {"quote": $scope.quote};

                        $scope.addSection('intro');
                        $scope.addSection('important_notes');
                        $scope.addService();
                        $scope.newQuote                 = true;
                    }
                }],
        templateUrl: '/static/quotes/html/qt_quote_form.html',
        link: function ($scope) {

            if($scope.newQuote){
                //$scope.quoteform.$show();
            }

            $scope.checkClient = function (data){
                if (!data) {
                  return "Plase select a client";
                }
            }

            $scope.dynamicPopover = {
                translationTemplateUrl: 'translationTemplate.html',
                serviceTemplateUrl: 'serviceTemplate.html'
            };

            $scope.changeLanguage = function (lang) {
                $scope.language = lang;
            };

            $scope.addLanguage = function (lang) {
                $scope.language_list[lang] = $scope.quoteLanguage[lang];
            };

            $scope.showRowForm = function (rowform) {
                if ($scope.quote.status != '2') {
                    rowform.$show();
                }
            };

            $scope.open = function () {
                $scope.modalInstance = $uibModal.open({
                    scope: $scope,
                    animation: true,
                    templateUrl: 'myModalContent.html'
                });
                return 0;
            };

        }
    };
    }]);