app = angular.module('gallant.directives.glForm', []);

app.directive('glRequiredErrors', function () {
    return {
        restrict: 'A',
        scope: {
            field: '=',
        },
        templateUrl: '/static/gallant/html/gl_required_errors.html',
    };
});

app.directive('glUltextInput', function () {
    return {
        restrict: 'A',
        scope: {
            name: '@',
            eid: '@',
            text: '=',
            language: '=',
            required: '@',
        },
        template: function ($scope, $element) {
            return '<input id="{{ eid }}" class="form-control" name="{{ name }}" maxlength="512"' +
                'type="text" ng-model="text[language]" ng-required="{{ required }}"/>';
        }
    };
})

app.directive('glUltextArea', function () {
    return {
        restrict: 'A',
        scope: {
            name: '@',
            eid: '@',
            text: '=',
            language: '=',
        },
        template: function ($scope, $element, $attrs) {
            return '<textarea id="{{ eid }}" class="form-control" cols="40" name="{{ name }}" rows="3" ' +
                'ng-model="text[language]"></textarea>';
        }
    };
});
