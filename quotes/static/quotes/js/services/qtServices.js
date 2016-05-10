app = angular.module('quotes.services.qtServices', []);

/* istanbul ignore next  */
app.factory("Quote", function ($resource) {
    // TODO: this shouldn't start with /en/

	return $resource("/en/quote/api/quote/:id", {client_id: '@client_id'}, {
		retrieve: {
		  method: 'GET',
		  params: {},
		  isArray: true
		},
		getUser: {
		  method: 'GET',
		  params: {},
		  url:"/en/quote/api/quote_token/:token"
		},
		query: {
		  method: 'GET',
		  params: {clients_only: true},
		  isArray: true,
		  url: '/en/quote/api/quote',
		},
		queryNC: {
		  method: 'GET',
		  params: {},
		  isArray: true,
		  url: '/en/quote/api/quote',	
		},
        fields: {
          method: 'GET',
          url: '/en/quote/api/quote/fields/ '
        },
        update: {
          method: 'PUT',
        },
        updateUser: {
          method: 'PATCH',
          url: '/en/quote/api/quote_client/:token',
        }
	});

});


/* istanbul ignore next  */
app.factory("Service", function ($resource) {
	//
	return $resource("/api/service/:id", {}, {
        fields: {
            method: 'GET',
			url: '/api/service/fields'
        },
        update: {
          method: 'PATCH',
          url: '/api/service/:id?user=:user',
        },
	});

});

/* istanbul ignore next  */
app.factory("Section", function ($resource) {
	//
	return $resource("/en/quote/api/section ", {}, {
        update: {
          method: 'PATCH',
          url: '/en/quote/api/section/:id?user=:user',
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
		  url: '/en/quote/api/quote_template?clients_only=False'			
		}
	});

});

/* istanbul ignore next */
app.factory('qtConstants', function () {
    return {
        QuoteStatus: {
			Draft: 0,
			Not_Sent: 1,
			Sent: 2,
			Viewed: 3,
			Superseded: 4,
			Accepted: 5,
			Rejected: 6,
        },
    };
});
