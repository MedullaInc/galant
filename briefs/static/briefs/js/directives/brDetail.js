app = angular.module('briefs.directives.brDetail', [
    'briefs.services.brServices',
    'ui.bootstrap',
    'gallant.directives.glForm',
    'gallant.services.glServices',
    'as.sortable'
]);

app.directive('brBriefDetail', ['Question', '$window', function (Question, $window) {
    return {
        restrict: 'A',
        scope: {
            object: '=?',
            endpoint: '=?',
            language: '=?',
            deleteObject: '&',
            submit: '&'
        },
        controller: ['$scope', '$attrs', '$filter', 'Brief', 'BriefTemplate', 'BriefAnswers', 'LANGUAGES', 'glValidate',
            function ($scope, $attrs, $filter, Brief, BriefTemplate, BriefAnswers, LANGUAGES, glValidate) {
                $scope.validate = glValidate;
                $scope.isTemplate = $attrs.isTemplate;
                $scope.submitForm = $scope.submit();

                var loadBriefAndTemplate = function(brief, template, language) {
                    $scope.brief = brief;
                    $scope.brief.quote = $attrs.quoteId;
                    $scope.brief.client = $attrs.clientId;
                    if (template) {
                        $scope.briefTemplate = template;
                        $scope.briefTemplate.brief = $scope.brief;
                        $scope.object = $scope.briefTemplate;

                        if (language) {
                            var lang = LANGUAGES.find(function (x) { return x.code == language;});
                            $scope.briefTemplate.languages = [lang];
                        }
                    } else {
                        $scope.object = $scope.brief;
                    }
                    if (!$scope.brief.questions) {
                        $scope.brief.questions = [];
                    } else {
                        $scope.brief.questions = $filter('orderBy')($scope.brief.questions, 'index');
                    }

                    if (!$scope.brief.field_choices) {
                        Brief.fields().$promise.then(function (fieldChoices) {
                            $scope.brief.field_choices = fieldChoices;
                        });
                    }
                };

                if ($attrs.isTemplate) {
                    $scope.endpoint = BriefTemplate;
                    if ($attrs.templateId) {
                        BriefTemplate.get({
                            id: $attrs.templateId
                        }).$promise.then(function (briefTemplate) {
                            loadBriefAndTemplate(briefTemplate.brief, briefTemplate);
                        });
                    } else {
                        if ($attrs.briefId) {
                            Brief.get({
                                id: $attrs.briefId
                            }).$promise.then(function (brief) {
                                var brief_lang = brief.language ? brief.language : $scope.language;
                                // we're creating a template from a saved brief, so delete IDs to create new one
                                delete brief.id;
                                brief.status = 0;
                                angular.forEach(brief.questions, function (q) {
                                    delete q.id;
                                });
                                loadBriefAndTemplate(brief, new BriefTemplate(), brief_lang);
                            });
                        } else {
                            loadBriefAndTemplate(new Brief(), new BriefTemplate(), $scope.language);

                        }
                    }
                } else {
                    $scope.endpoint = Brief;
                    if ($attrs.briefId) {
                        Brief.get({
                            id: $attrs.briefId
                        }).$promise.then(function (brief) {
                            if (brief.answered) {
                                BriefAnswers.query({
                                    brief_id: $attrs.briefId
                                }).$promise.then(function (answerList) {
                                    var answers = answerList[0].answers;
                                    angular.forEach(answers, function(a) {
                                        var question = brief.questions.find(function (q) {
                                            return q.id == a.question;
                                        });
                                        if (question) {
                                            question.answer = a;
                                        }
                                    });
                                    loadBriefAndTemplate(brief)
                                });
                            } else {
                                loadBriefAndTemplate(brief);
                            }
                        });
                    } else {
                        if ($attrs.templateId) {
                            BriefTemplate.get({
                                id: $attrs.templateId
                            }).$promise.then(function (briefTemplate) {
                                loadBriefAndTemplate(briefTemplate.brief);
                                delete $scope.brief.id;
                                angular.forEach($scope.brief.questions, function (q) {
                                    delete q.id;
                                });
                                if ($scope.briefForm.$show) {
                                    $scope.briefForm.$show();
                                }
                            });
                        } else {
                            loadBriefAndTemplate(new Brief());
                        }
                    }
                }

                $scope.dragControlListeners = {
                    accept: function (sourceItemHandleScope, destSortableScope) {
                        return sourceItemHandleScope.itemScope.sortableScope.$id === destSortableScope.$id;
                    }
                };

                $scope.storeBrief = function() {
                    $scope.storedBrief = JSON.stringify($scope.brief);
                };

                $scope.loadStoredBrief = function() {
                    $scope.brief = JSON.parse($scope.storedBrief);
                };
            }],
        templateUrl: '/static/briefs/html/br_brief_detail.html',
        link: function ($scope) {
            $scope.addQuestion = function (type) {
                var question = new Question();
                if (type == 'multi') {
                    question.type = 'MultipleChoiceQuestion';
                    question.choices = [{}, {}];
                } else {
                    question.type = 'TextQuestion';
                }
                question.index = $scope.brief.questions.length;
                if (!$scope.briefForm.$visible) {
                    $scope.briefForm.$show();
                }
                $scope.brief.questions.push(question);
            };

            $scope.removeQuestion = function (question) {
                if ($window.confirm('Remove question?')) {
                    var index = $scope.brief.questions.indexOf(question);
                    $scope.brief.questions.splice(index, 1);
                }
            };

            $scope.showButtons = function () {
                return (typeof $scope.addQuestion === 'function');
            };

            var submitWithoutOnAfterSave = function(form) {
                var tmpFn = form.$onaftersave;
                form.$onaftersave = angular.noop;
                form.$submit();
                form.$onaftersave = tmpFn;
            };

            $scope.setLanguage = function (language) {
                var initVis = $scope.briefForm.$visible;
                if (initVis) {
                    submitWithoutOnAfterSave($scope.briefForm);
                }
                if (!$scope.briefForm.$visible) {
                    $scope.language = language;
                    if (initVis)
                        $scope.briefForm.$show();
                }
            };

            $scope.addLanguage = function (language) {
                if ($scope.briefForm.$visible) {
                    submitWithoutOnAfterSave($scope.briefForm);
                }

                if (!$scope.briefForm.$visible) {
                    $scope.briefTemplate.languages.push(language);
                    $scope.setLanguage(language.code);
                    $scope.briefForm.$show();
                }
            };
        }
    };
}]);


app.directive('brQuestionDetail', ['$window', 'glValidate', function ($window, glValidate) {
    return {
        restrict: 'A',
        scope: {
            question: '=',
            language: '=',
            errors: '=',
            answered: '=',
            form: '=',
        },
        controller: function ($scope) {
            $scope.validate = glValidate;

            $scope.dragControlListeners = {
                accept: function (sourceItemHandleScope, destSortableScope) {
                    return sourceItemHandleScope.itemScope.sortableScope.$id === destSortableScope.$id;
                }
            };
        },
        link: function ($scope) {
            var template = '/static/briefs/html/br_question_detail.html';
            if ($scope.question.type == 'MultipleChoiceQuestion') {
                template = '/static/briefs/html/br_multiquestion_detail.html';
            }
            $scope.myTemplate = template;

            $scope.addChoice = function () {
                if ($scope.question.choices) {
                    $scope.question.choices.push({});
                }
            };
            $scope.removeChoice = function ($index) {
                if ($window.confirm('Remove choice?')) {
                    $scope.question.choices.splice($index, 1);
                }
            };
        },
        template: "<div ng-include='myTemplate'></div>",
    };
}]);
