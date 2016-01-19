app = angular.module('briefs.directives.brDetail', [
    'briefs.services.brServices'
]);

app.directive('brBriefDetail', ['Question', function (Question) {
    return {
        restrict: 'A',
        scope: {
            brief: '=',
            endpoint: '=',
            language: '='
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
        }
    };
}]);
