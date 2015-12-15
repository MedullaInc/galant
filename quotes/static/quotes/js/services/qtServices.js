app = angular.module('quotes.services.qtServices', []);

app.factory("Quote", function ($resource) {
    // TODO: this shouldn't start with /en/

	return $resource("/en/quote/api/quote/:id", {}, {
		query: {
		  method: 'GET',
		  params: {},
		  isArray: true
		},
		all: {
		  method: 'GET',
		  params: {},
		  isArray: true,
		  url: '/en/quote/api/quote/'			
		}
	});

});

app.factory("Service", function ($resource) {
    // TODO: this shouldn't start with /en/

	return $resource("/api/service/fields", {}, {
        fields: {
            method: 'GET',
        },
	});

});

app.factory("QuoteTemplate", function ($resource) {
    return $resource("/en/quote/api/template/:id");
});


