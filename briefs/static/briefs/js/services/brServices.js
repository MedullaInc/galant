app = angular.module('briefs.services.brServices', []);

/* istanbul ignore next  */
app.factory("Brief", ['$resource', function ($resource) {
    // TODO: this shouldn't start with /en/
    return $resource("/en/briefs/api/brief/:id", {}, {
        fields: {
          method: 'GET',
          url: '/en/briefs/api/brief/fields/ '
        },
    });
}]);

/* istanbul ignore next  */
app.factory("BriefTemplate", ['$resource', function ($resource) {
    return $resource("/en/briefs/api/template/:id");
}]);

/* istanbul ignore next  */
app.factory("Question", ['$resource', function ($resource) {
    return $resource("/en/briefs/api/question/:id");
}]);

/* istanbul ignore next  */
app.factory("BriefAnswers", ['$resource', function ($resource) {
    return $resource("/en/briefs/api/briefanswers/:id");
}]);
