app = angular.module('briefs.services.brServices', []);

app.factory("Brief", function ($resource) {
    // TODO: this shouldn't start with /en/
    return $resource("/en/briefs/api/brief/:id");
});

app.factory("BriefTemplate", function ($resource) {
    return $resource("/en/briefs/api/template/:id");
});

app.factory("Question", function ($resource) {
    return $resource("/en/briefs/api/question/:id");
});
