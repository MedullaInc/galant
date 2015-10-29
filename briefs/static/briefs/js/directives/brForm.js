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
            },
            link: function ($scope) {
                var template = '/static/briefs/html/question_form.html';
                if ($scope.question.type == 'MultipleChoiceQuestion') {
                console.log($scope.question.choices);
                    template = '/static/briefs/html/multiquestion_form.html';
                }
                $scope.myTemplate = template;
            },
            template: "<div ng-include='myTemplate'></div>",
        };
    }).directive('brBriefForm', ['Briefs', function (Briefs) {
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
                Briefs.get({
                    id: $attrs.briefId
                }, function (result) {
                    $scope.brief = result;
                });
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
