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


app.constant('LANGUAGES', [
    {'code': 'af', 'name': 'Afrikaans'},
    {'code': 'ar', 'name': 'Arabic'},
    {'code': 'ast', 'name': 'Asturian'},
    {'code': 'az', 'name': 'Azerbaijani'},
    {'code': 'bg', 'name': 'Bulgarian'},
    {'code': 'be', 'name': 'Belarusian'},
    {'code': 'bn', 'name': 'Bengali'},
    {'code': 'br', 'name': 'Breton'},
    {'code': 'bs', 'name': 'Bosnian'},
    {'code': 'ca', 'name': 'Catalan'},
    {'code': 'cs', 'name': 'Czech'},
    {'code': 'cy', 'name': 'Welsh'},
    {'code': 'da', 'name': 'Danish'},
    {'code': 'de', 'name': 'German'},
    {'code': 'el', 'name': 'Greek'},
    {'code': 'en', 'name': 'English'},
    {'code': 'en-au', 'name': 'Australian English'},
    {'code': 'en-gb', 'name': 'British English'},
    {'code': 'eo', 'name': 'Esperanto'},
    {'code': 'es', 'name': 'Spanish'},
    {'code': 'es-ar', 'name': 'Argentinian Spanish'},
    {'code': 'es-co', 'name': 'Colombian Spanish'},
    {'code': 'es-mx', 'name': 'Mexican Spanish'},
    {'code': 'es-ni', 'name': 'Nicaraguan Spanish'},
    {'code': 'es-ve', 'name': 'Venezuelan Spanish'},
    {'code': 'et', 'name': 'Estonian'},
    {'code': 'eu', 'name': 'Basque'},
    {'code': 'fa', 'name': 'Persian'},
    {'code': 'fi', 'name': 'Finnish'},
    {'code': 'fr', 'name': 'French'},
    {'code': 'fy', 'name': 'Frisian'},
    {'code': 'ga', 'name': 'Irish'},
    {'code': 'gd', 'name': 'Scottish Gaelic'},
    {'code': 'gl', 'name': 'Galician'},
    {'code': 'he', 'name': 'Hebrew'},
    {'code': 'hi', 'name': 'Hindi'},
    {'code': 'hr', 'name': 'Croatian'},
    {'code': 'hu', 'name': 'Hungarian'},
    {'code': 'ia', 'name': 'Interlingua'},
    {'code': 'id', 'name': 'Indonesian'},
    {'code': 'io', 'name': 'Ido'},
    {'code': 'is', 'name': 'Icelandic'},
    {'code': 'it', 'name': 'Italian'},
    {'code': 'ja', 'name': 'Japanese'},
    {'code': 'ka', 'name': 'Georgian'},
    {'code': 'kk', 'name': 'Kazakh'},
    {'code': 'km', 'name': 'Khmer'},
    {'code': 'kn', 'name': 'Kannada'},
    {'code': 'ko', 'name': 'Korean'},
    {'code': 'lb', 'name': 'Luxembourgish'},
    {'code': 'lt', 'name': 'Lithuanian'},
    {'code': 'lv', 'name': 'Latvian'},
    {'code': 'mk', 'name': 'Macedonian'},
    {'code': 'ml', 'name': 'Malayalam'},
    {'code': 'mn', 'name': 'Mongolian'},
    {'code': 'mr', 'name': 'Marathi'},
    {'code': 'my', 'name': 'Burmese'},
    {'code': 'nb', 'name': 'Norwegian Bokmal'},
    {'code': 'ne', 'name': 'Nepali'},
    {'code': 'nl', 'name': 'Dutch'},
    {'code': 'nn', 'name': 'Norwegian Nynorsk'},
    {'code': 'os', 'name': 'Ossetic'},
    {'code': 'pa', 'name': 'Punjabi'},
    {'code': 'pl', 'name': 'Polish'},
    {'code': 'pt', 'name': 'Portuguese'},
    {'code': 'pt-br', 'name': 'Brazilian Portuguese'},
    {'code': 'ro', 'name': 'Romanian'},
    {'code': 'ru', 'name': 'Russian'},
    {'code': 'sk', 'name': 'Slovak'},
    {'code': 'sl', 'name': 'Slovenian'},
    {'code': 'sq', 'name': 'Albanian'},
    {'code': 'sr', 'name': 'Serbian'},
    {'code': 'sr-latn', 'name': 'Serbian Latin'},
    {'code': 'sv', 'name': 'Swedish'},
    {'code': 'sw', 'name': 'Swahili'},
    {'code': 'ta', 'name': 'Tamil'},
    {'code': 'te', 'name': 'Telugu'},
    {'code': 'th', 'name': 'Thai'},
    {'code': 'tr', 'name': 'Turkish'},
    {'code': 'tt', 'name': 'Tatar'},
    {'code': 'udm', 'name': 'Udmurt'},
    {'code': 'uk', 'name': 'Ukrainian'},
    {'code': 'ur', 'name': 'Urdu'},
    {'code': 'vi', 'name': 'Vietnamese'},
    {'code': 'zh-hans', 'name': 'Simplified Chinese'},
    {'code': 'zh-hant', 'name': 'Traditional Chinese'},
]);


app.directive('glLanguageForm', ['LANGUAGES', function (LANGUAGES) {
    return {
        controller: ['$scope', function ($scope) {
            $scope.languages = LANGUAGES;
        }],
        templateUrl: '/static/gallant/html/gl_language_form.html',
    };
}]);