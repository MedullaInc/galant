angular.module('briefs.directives.brForm', [])
    .directive('brRequiredErrors', function () {
        return {
            restrict: 'A',
            scope: {
                field: '=',
            },
            templateUrl: '/static/briefs/html/required_errors.html',
        };
    })
    .directive('brQuestionForm', function () {
        return {
            restrict: 'A',
            scope: {
                question: '=',
                language: '=',
                forms: '=',
                removeQuestion: '&'
            },
            link: function ($scope, $element) {
                var template = '/static/briefs/html/question_form.html';
                if ($scope.question.type == 'MultipleChoiceQuestion') {
                    template = '/static/briefs/html/multiquestion_form.html';
                }
                $scope.myTemplate = template;

                $scope.remove = function () {
                    $element.remove();
                    $scope.removeQuestion()($scope.question);
                }
            },
            template: "<div ng-include='myTemplate'></div>",
        };
    }).directive('brBriefForm', ['Brief', 'Question', function (Brief, Question) {
        return {
            restrict: 'A',
            require: 'brQuestionForm',
            scope: {
                brief: '=',
                language: '=',
                forms: '=',
            },
            templateUrl: '/static/briefs/html/brief_form.html',
            controller: function ($scope, $element, $attrs) {
                Brief.get({
                    id: $attrs.briefId
                }, function (result) {
                    $scope.brief = result;
                }, function (errorResult) {
                    $scope.brief = new Brief();
                    $scope.brief.questions = [];
                });

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
            }
        };
    }]).directive('brUltextInput', function () {
        return {
            restrict: 'A',
            scope: {
                name: '@',
                text: '=',
                language: '=',
                required: '@',
            },
            template: function ($scope) {
                return '<input class="form-control" name="{{ name }}" maxlength="512"' +
                    'type="text" ng-model="text[language]" ng-required="{{ required }}"/>';
            }
        };
    }).directive('brUltextArea', function () {
        return {
            restrict: 'A',
            scope: {
                name: '@',
                text: '=',
                language: '=',
            },
            template: function ($scope) {
                return '<textarea class="form-control" cols="40" name="{{ name }}" rows="3" ' +
                    'ng-model="text[language]"></textarea>';
            }
        };
    });
