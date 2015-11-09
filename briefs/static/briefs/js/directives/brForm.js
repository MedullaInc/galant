app = angular.module('briefs.directives.brForm', [
    'briefs.services.brServices',
    'gallant.directives.glForm'
]);

app.directive('brQuestionForm', function () {
    return {
        restrict: 'A',
        scope: {
            question: '=',
            language: '=',
            forms: '=',
            removeQuestion: '&'
        },
        link: function ($scope, $element) {
            var template = '/static/briefs/html/br_question_form.html';
            if ($scope.question.type == 'MultipleChoiceQuestion') {
                template = '/static/briefs/html/br_multiquestion_form.html';
            }
            $scope.myTemplate = template;

            $scope.remove = function () {
                if (confirm('Remove question?')) {
                    $element.remove();
                    $scope.removeQuestion()($scope.question);
                }
            }

            $scope.addChoice = function () {
                if ($scope.question.choices) {
                    $scope.question.choices.push(null);
                }
            }
            $scope.removeChoice = function ($index) {
                if (confirm('Remove choice?')) {
                    $scope.question.choices.splice($index, 1);
                }
            }
        },
        template: "<div ng-include='myTemplate'></div>",
    };
});

app.directive('brBriefForm', ['Question', function (Question) {
    return {
        restrict: 'A',
        scope: {
            brief: '=',
            endpoint: '=',
            language: '=',
            forms: '=',
        },
        controller: ['$scope', '$attrs', 'Brief', 'BriefTemplate',
            function ($scope, $attrs, Brief, BriefTemplate) {
                $scope.endpoint = Brief;
                if ($attrs.briefId) {
                    Brief.get({
                        id: $attrs.briefId
                    }).$promise.then(function (brief) {
                            $scope.brief = brief;
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
                            });
                    } else {
                        $scope.brief = new Brief();
                        $scope.brief.questions = [];
                        $scope.brief.quote = $attrs.quoteId;
                        $scope.brief.client = $attrs.clientId;
                    }
                }
            }],
        templateUrl: '/static/briefs/html/br_brief_form.html',
        link: function ($scope) {
            $scope.addQuestion = function (type) {
                var question = new Question();
                if (type == 'multi') {
                    question.type = 'MultipleChoiceQuestion';
                    question.choices = [{}, {}]
                } else {
                    question.type = 'TextQuestion';
                }
                question.index = $scope.brief.questions.length;
                $scope.brief.questions.push(question);
            }

            $scope.removeQuestion = function (question) {
                var index = $scope.brief.questions.indexOf(question);
                $scope.brief.questions.splice(index, 1);
            }

            $scope.showButtons = function () {
                return (typeof $scope.addQuestion === 'function');
            }
        }
    };
}]);
