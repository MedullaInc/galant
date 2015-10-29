angular.module('briefs.directives.brBriefForm', [])
  .directive('brQuestionForm', function () {
    return {
        restrict: 'A',
        scope: {
            question: '=',
            language: '=',
            forms: '=',
        },
        templateUrl: '/static/briefs/html/question_form.html',
    };
}).directive('brBriefForm', function () {
    return {
        restrict: 'A',
        scope: {
            question: '=',
            language: '=',
            forms: '=',
        },
        templateUrl: '/static/briefs/html/brief_form.html',
    };
}).directive('brUltextInput', function () {
    return {
        restrict: 'A',
        scope: {
            text: '=',
            language: '@',
        },
        template: function($scope) {
            return '<input class="form-control" maxlength="512" type="text" ng-model="text[language]"/>';
        }
    };
});