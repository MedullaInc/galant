describe('brDetail', function () {
    var $rootScope;
    var $compile;
    var $scope;

    beforeEach(function () {
        module('briefs.directives.brDetail');
        module('staticNgTemplates');

        angular.module('ui.bootstrap', []);
        angular.module('brief.services.brServices', []);
        module('brief.services.brServices', function ($provide) {
            $provide.factory('Question', function ($q) {
                var Question = function () { return {id: 0}; };
                Question.get = function () { return {$promise: $q.when([{id: 0}])}; };
                return Question;
            });

            $provide.factory('Brief', function ($q) {
                var Brief = function () { return {id: 0}; };
                Brief.get = function () { return {$promise: $q.when({id: 0, answered: true, questions: [{}]})}; };
                Brief.fields = function () { return {$promise: $q.when({})}; };
                return Brief;
            });

            $provide.factory('BriefAnswers', function ($q) {
                var BriefAnswers = function () { return {id: 0}; };
                BriefAnswers.query = function () { return {$promise: $q.when([{id: 0, answers: [{}]}])}; };
                return BriefAnswers;
            });

            $provide.factory('BriefTemplate', function ($q) {
                var BriefTemplate = function () {};
                BriefTemplate.get = function () { return {$promise: $q.when({id: 0, languages: [], brief: {
                    id: 0,
                    questions: [{}]
                }})}; };
                return BriefTemplate;
            });

            $provide.factory('glValidate', function ($q) { return {}; });

            $provide.factory('$window', function () { return {confirm: function(m) { return true; }}; });
        });

        inject(function (_$rootScope_, _$compile_) {
            // The injector unwraps the underscores (_) from around the parameter names when matching
            $rootScope = _$rootScope_;
            $compile = _$compile_;
        });

        $scope = $rootScope.$new();
    });

    describe('brQuestionDetail', function () {
        beforeEach(function () {
            $scope.question = {type: 'TextQuestion'};
            $scope.language = 'en';
        });

        it('compiles', function () {
            var element = $compile('<div br-question-detail question="question"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 3)).toEqual('<!-');
        });

        it('adds and removes choices', function () {
            $scope.question.choices = [];
            var element = $compile('<div br-question-detail question="question"></div>')($scope);
            $scope.$digest();

            element.isolateScope().addChoice();
            expect($scope.question.choices.length).toEqual(1);

            var tmp = window.confirm;
            window.confirm = function (str) { return true; };
            element.isolateScope().removeChoice(0);
            window.confirm = tmp;
            expect($scope.question.choices.length).toEqual(0);
        });
    });

    describe('brBriefDetail', function () {
        it('compiles', function () {
            var element = $compile('<div br-brief-detail></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<script ');
        });

        it('compiles with brief id', function () {
            var element = $compile('<div br-brief-detail brief-id="0"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<script ');
        });

        it('compiles with brief template id', function () {
            var element = $compile('<div br-brief-detail template-id="0" quote-id="0" client-id="0"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<script ');
        });

        it('compiles with brief template id and is-template', function () {
            var element = $compile('<div br-brief-detail template-id="0" is-template="true"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<script ');
        });

        it('compiles  with brief id and is-template', function () {
            var element = $compile('<div br-brief-detail brief-id="0" is-template="true"></div>')($scope);
            $scope.$digest();
            expect(element.html().substring(0, 8)).toEqual('<script ');
        });

        it('adds question', function () {
            $scope.brief = {};
            var element = $compile('<div br-brief-detail object="brief"></div>')($scope);
            $scope.$digest();
            element.isolateScope().briefForm = {$show: function() {}};

            element.isolateScope().addQuestion();
            element.isolateScope().addQuestion('multi');
            expect($scope.brief.questions.length).toEqual(2);
            element.isolateScope().removeQuestion($scope.brief.questions[0]);
            expect($scope.brief.questions.length).toEqual(1);
        });

        it('sets language', function () {
            $scope.language = 'en';
            var element = $compile('<div br-brief-detail object="brief" language="language"></div>')($scope);
            $scope.$digest();
            element.isolateScope().briefForm = {$show: function() {}, $visible: true, $submit: function() {}};
            element.isolateScope().brief = {title: {en: ''}};

            element.isolateScope().setLanguage('en');
            expect(element.isolateScope().language).toEqual('en');
        });

        it('adds language', function () {
            $scope.language = 'en';;
            var element = $compile(
                '<div br-brief-detail object="brief" is-template="true" language="language"></div>'
            )($scope);
            $scope.$digest();
            element.isolateScope().briefForm = {$show: function() {}};
            element.isolateScope().brief = {title: {en: ''}};

            element.isolateScope().addLanguage({'code': 'es', 'name': 'Spanish'});
            expect(element.isolateScope().briefTemplate.languages.length).toEqual(2);
        });

        it('stores and loads brief', function () {
            var element = $compile('<div br-brief-detail object="brief"></div>')($scope);
            $scope.$digest();
            element.isolateScope().brief = {id: 11};
            element.isolateScope().storeBrief();
            element.isolateScope().brief = {id: 12};
            element.isolateScope().loadStoredBrief();
            expect(element.isolateScope().brief.id).toEqual(11);

        });
    });
});
