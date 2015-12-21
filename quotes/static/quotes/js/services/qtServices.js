app = angular.module('quotes.services.qtServices', []);

/* istanbul ignore next  */
app.factory("Quote", function ($resource) {
    // TODO: this shouldn't start with /en/

	return $resource("/en/quote/api/quote/:id", {}, {
		retrieve: {
		  method: 'GET',
		  params: {},
		  isArray: true
		},
		query: {
		  method: 'GET',
		  params: {},
		  isArray: true,
		  url: '/en/quote/api/quote/'			
		},
        fields: {
          method: 'GET',
          url: '/en/quote/api/quote/fields/ '
        },
	});

});

/* istanbul ignore next  */
app.factory("Service", function ($resource) {
	//

	return $resource("/api/service/fields", {}, {
        fields: {
            method: 'GET',
        },
	});

});

/* istanbul ignore next  */
app.factory("Client", function ($resource) {
    // TODO: this shouldn't start with /en/

	return $resource("/api/client ", {}, {
        query: {
            method: 'GET',
            isArray: true,
        },
	});

});

/* istanbul ignore next  */
app.factory("QuoteTemplate", function ($resource) {
    // TODO: this shouldn't start with /en/

	return $resource("/en/quote/api/quote_template/:id", {}, {
		retrieve: {
		  method: 'GET',
		  params: {},
		  isArray: true
		},
		query: {
		  method: 'GET',
		  params: {},
		  isArray: true,
		  url: '/en/quote/api/quote_template/'			
		}
	});

});


