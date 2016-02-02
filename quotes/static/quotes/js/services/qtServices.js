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
        update: {
          method: 'PATCH',
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
        get: {
          method: 'GET',
          url: '/api/service ',
          isArray: true
        },
        update: {
          method: 'PATCH',
          url: '/api/service/:id ',
        },
	});

});

/* istanbul ignore next  */
app.factory("Section", function ($resource) {
	//
	return $resource("/en/quote/api/section ", {}, {
        update: {
          method: 'PATCH',
          url: '/en/quote/api/section/:id ',
        },
	});

});


/* istanbul ignore next  */
app.factory("Client", function ($resource) {
    // TODO: this shouldn't start with /en/

	return $resource("/api/client ", {}, {
        get: {
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


