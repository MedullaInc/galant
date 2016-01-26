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
        template: '<input id="{{ eid }}" class="form-control" name="{{ name }}"' +
                'type="text" ng-model="text[language]" required="{{ required }}"/>',
    };
});

app.directive('glUltextArea', function () {
    return {
        restrict: 'A',
        scope: {
            name: '@',
            eid: '@',
            text: '=',
            language: '=',
            required: '@',
        },
        template: '<textarea id="{{ eid }}" class="form-control" cols="40" name="{{ name }}" rows="3" ' +
                'ng-model="text[language]" required="{{ required }}"></textarea>',
    };
});
