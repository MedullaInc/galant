app = angular.module('briefs.directives.brDetail', [
    'briefs.services.brServices',
    'ui.bootstrap'
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
                if ($attrs.isTemplate) {
                    $scope.endpoint = BriefTemplate;
                    if ($attrs.templateId) {
                        BriefTemplate.get({
                            id: $attrs.templateId
                        }).$promise.then(function (briefTemplate) {
                            $scope.briefTemplate = briefTemplate;
                            $scope.brief = $scope.briefTemplate.brief;
                            $scope.brief.quote = $attrs.quoteId;
                            $scope.brief.client = $attrs.clientId;
                            $scope.object = $scope.briefTemplate;
                        });
                    } else {
                        if ($attrs.briefId) {
                            Brief.get({
                                id: $attrs.briefId
                            }).$promise.then(function (brief) {
                                $scope.brief = brief;
                                $scope.briefTemplate = new BriefTemplate();
                                var brief_lang = $scope.brief.language ? $scope.brief.language : $scope.language;
                                var lang = LANGUAGES.find(function (x) {
                                    return x.code == brief_lang;
                                });
                                $scope.briefTemplate.languages = [lang];
                                $scope.briefTemplate.brief = $scope.brief;
                                $scope.object = $scope.briefTemplate;
                            });
                        } else {
                            $scope.brief = new Brief();
                            $scope.brief.questions = [];
                            $scope.brief.quote = $attrs.quoteId;
                            $scope.brief.client = $attrs.clientId;
                            $scope.briefTemplate = new BriefTemplate();
                            var lang = LANGUAGES.find(function (x) { return x.code == $scope.language;});
                            $scope.briefTemplate.languages = [lang];
                            $scope.briefTemplate.brief = $scope.brief;
                            $scope.object = $scope.briefTemplate;
                        }
                    }
                } else {
                    $scope.endpoint = Brief;
                    if ($attrs.briefId) {
                        Brief.get({
                            id: $attrs.briefId
                        }).$promise.then(function (brief) {
                            $scope.brief = brief;
                            $scope.object = $scope.brief;
                        });
                    } else {
                        if ($attrs.templateId) {
                            BriefTemplate.get({
                                id: $attrs.templateId
                            }).$promise.then(function (briefTemplate) {
                                $scope.brief = briefTemplate.brief;
                                delete $scope.brief.id;
                                angular.forEach($scope.brief.questions, function (q) {
                                    delete q.id;
                                });
                                $scope.brief.quote = $attrs.quoteId;
                                $scope.brief.client = $attrs.clientId;
                                $scope.object = $scope.brief;
                            });
                        } else {
                            $scope.brief = new Brief();
                            $scope.brief.questions = [];
                            $scope.brief.quote = $attrs.quoteId;
                            $scope.brief.client = $attrs.clientId;
                            $scope.object = $scope.brief;
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
