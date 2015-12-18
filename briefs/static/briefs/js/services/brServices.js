app = angular.module('briefs.services.brServices', []);

/* istanbul ignore next  */
app.factory("Brief", function ($resource) {
    // TODO: this shouldn't start with /en/
    return $resource("/en/briefs/api/brief/:id");
});

/* istanbul ignore next  */
app.factory("BriefTemplate", function ($resource) {
    return $resource("/en/briefs/api/template/:id");
});

/* istanbul ignore next  */
app.factory("Question", function ($resource) {
    return $resource("/en/briefs/api/question/:id");
});
