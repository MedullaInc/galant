app = angular.module('briefs.directives.brDetail', [
    'briefs.services.brServices',
    'ui.bootstrap',
    'gallant.directives.glForm'
]);

app.directive('brBriefDetail', ['Question', function (Question) {
    return {
        restrict: 'A',
        scope: {
            object: '=',
            endpoint: '=',
            language: '=',
            deleteObject: '&'
        },
        controller: ['$scope', '$attrs', 'Brief', 'BriefTemplate', 'LANGUAGES',
            function ($scope, $attrs, Brief, BriefTemplate, LANGUAGES) {
                var loadBriefAndTemplate = function(brief, template, language) {
                    $scope.brief = brief
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
                            loadBriefAndTemplate(brief);
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
                            });
                        } else {
                            loadBriefAndTemplate(new Brief());
                        }
                    }
                }
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
                $scope.brief.questions.push(question);
            };

            $scope.removeQuestion = function (question) {
                var index = $scope.brief.questions.indexOf(question);
                $scope.brief.questions.splice(index, 1);
            };

            $scope.showButtons = function () {
                return (typeof $scope.addQuestion === 'function');
            };

            $scope.setLanguage = function (language) {
                $scope.language = language;
            };

            $scope.addLanguage = function (language) {
                $scope.briefTemplate.languages.push(language);
            };
        }
    };
}]);


app.directive('brQuestionDetail', function (Question) {
    return {
        restrict: 'A',
        scope: {
            question: '=',
            language: '=',
            errors: '=',
            answered: '=',
            removeQuestion: '&'
        },
        link: function ($scope, $element) {
            var template = '/static/briefs/html/br_question_detail.html';
            if ($scope.question.type == 'MultipleChoiceQuestion') {
                template = '/static/briefs/html/br_multiquestion_detail.html';
            }
            $scope.myTemplate = template;

            $scope.remove = function () {
                if (confirm('Remove question?')) {
                    $element.remove();
                    $scope.removeQuestion()($scope.question);
                }
            };

            $scope.addChoice = function () {
                if ($scope.question.choices) {
                    $scope.question.choices.push(null);
                }
            };
            $scope.removeChoice = function ($index) {
                if (confirm('Remove choice?')) {
                    $scope.question.choices.splice($index, 1);
                }
            };
        },
        template: "<div ng-include='myTemplate'></div>",
    };
});
