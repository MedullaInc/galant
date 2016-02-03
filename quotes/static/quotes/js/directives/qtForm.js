app = angular.module('quotes.directives.qtForm', [
    'quotes.services.qtServices',
    'gallant.directives.glForm',
    'ui.bootstrap',
    'as.sortable']);

app.filter('cut', function () {
        return function (value, wordwise, max, tail) {
            if (!value) return '';

            max = parseInt(max, 10);
            if (!max) return value;
            if (value.length <= max) return value;

            value = value.substr(0, max);
            if (wordwise) {
                var lastspace = value.lastIndexOf(' ');
                if (lastspace != -1) {
                    value = value.substr(0, lastspace);
                }
            }

            return value + (tail || '');
        };
    })

    .directive('qtQuoteForm', ['Quote', 'Service','Section', 'Client', '$filter', '$uibModal', function (Quote, Service, Section, Client, $filter, $uibModal) {
        return {
            restrict: 'A',
            scope: {
                quote: '=',
                quoteTemplate: '=',
                endpoint: '=',
                language: '=',
                forms: '=',
                boolTemplate: '='
            },
            controller: ['$scope', '$attrs', '$filter', '$window', 'Quote', 'Service', 'Section', 'QuoteTemplate', 'Client',
                function ($scope, $attrs, $filter, $window, Quote, Service, Section, QuoteTemplate, Client) {
                    $scope.isCollapsed = false;
                    $scope.quoteFields = [];
                    $scope.quoteStatus = {};
                    $scope.quoteLanguage = {};
                    $scope.services = [];
                    $scope.sections = [];
                    $scope.serviceFields = [];
                    $scope.language_list = {};

                    $window.onbeforeunload = function () { 
                        $scope.quote.session_duration = ((new Date() - $scope.$parent.startTime)/1000 );
                        $scope.quote.views = $scope.quote.views+1;
                        Quote.update({id: $scope.quote.id}, $scope.quote);
                    }

                    $scope.addSection = function (section_name) {
                        var name = "";
                        var counter;

                        if (section_name) {
                            name = section_name;
                        } else {
                            counter = $scope.quote.sections.length;
                            name = "section_" + (counter++);
                        }

                        $scope.inserted = {
                            title: {},
                            text: {},
                            name: name,
                            index: counter,
                            views: 0,
                        };
                        $scope.quote.sections.push($scope.inserted);
                    };

                    $scope.addService = function (service) {
                        if (service) {
                            $scope.insertedService = service;
                            $scope.modalInstance.close();
                        } else {
                            $scope.insertedService = {
                                cost: {
                                    amount: "0",
                                    currency: "USD"
                                },
                                user: $scope.quote.user,
                                name: "",
                                notes: Array[0],
                                parent: null,
                                quantity: "",
                                type: "",
                                views: 0,
                            };
                        }
                        $scope.quote.services.push($scope.insertedService);
                    };

                    $scope.addLanguage = function (lang) {
                        $scope.language_list[lang] = $scope.quoteLanguage[lang];
                    };

                    Client.get().$promise.then(function (clients) {
                        $scope.clients = clients;
                    });

                    Quote.fields().$promise.then(function (fields) {
                        $scope.quoteStatus = fields.status;
                        $scope.quoteLanguage = fields.language;
                    });

                    Service.get().$promise.then(function (services) {
                        $scope.services = services;
                    });

                    Service.fields({}).$promise.then(function (fields) {
                        $scope.serviceFields = fields.type;
                    });

                    $scope.boolTemplate = $attrs.boolTemplate;
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
                    } else {
                        if ($attrs.templateId) {
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
                            $scope.quote = {
                                "id": null,
                                "user": $attrs.userId,
                                "name": "New Quote",
                                "client": $attrs.clientId,
                                "sections": [],
                                "services": [],
                                "status": "0",
                                "modified": "",
                                "token": "",
                                "parent": null,
                                "projects": [],
                                "views": 0,
                                "session_duration": 0.0,
                            };

                            $scope.quoteTemplate = {
                                "quote": $scope.quote
                            };

                            $scope.addSection('intro');
                            $scope.addSection('important_notes');
                            $scope.addService();
                        }

                    }
                }
            ],
            templateUrl: '/static/quotes/html/qt_quote_form.html',
            link: function ($scope) {

                $scope.dynamicPopover = {
                    translationTemplateUrl: 'translationTemplate.html',
                    serviceTemplateUrl: 'serviceTemplate.html'
                };

                $scope.showService = function (service){
                    id = service.id;
                    service.views = service.views+1;
                    Service.update({id: id}, service);
                }

                $scope.showSection = function (section){
                    id = section.id;
                    section.views = section.views+1;
                    Section.update({id: id}, section);                       
                }

                $scope.changeLanguage = function (lang) {
                    $scope.language = lang;
                };

                $scope.removeService = function (index) {
                    $scope.quote.services.splice(index, 1);
                };

                $scope.showType = function (service) {
                    if (service) {
                        return $scope.serviceFields[service.type];
                    }
                };

                $scope.getTotal = function () {
                    if ($scope.quote) {
                        if ($scope.quote.services) {
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
                };

                $scope.showRowForm = function (rowform) {
                    if ($scope.quote.status != '2') {
                        rowform.$show();
                    }
                };

                $scope.removeSection = function (index) {
                    $scope.quote.sections.splice(index, 1);
                };

                $scope.open = function () {
                    $scope.modalInstance = $uibModal.open({
                        scope: $scope,
                        animation: true,
                        templateUrl: 'myModalContent.html'
                    });
                    return 0;
                };

                $scope.dragControlListeners = {
                    orderChanged: function (event) {
                    }
                };
            }
        };
    }]);