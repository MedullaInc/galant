app = angular.module('gallant.services.glServices', ['ngResource']);

/* istanbul ignore next */
app.factory('Client', function ($resource) {
    return $resource('/api/client/:id', {}, {
        fields: {
            method: 'GET',
            url: '/api/client/fields'
        },
        update: {
          method: 'PATCH',
        },
    });
});

/* istanbul ignore next */
app.factory('ClientQuote', function ($resource) {
    return $resource('/en/quote/api/quote/:id');
});

/* istanbul ignore next */
app.factory('Payment', function ($resource) {
    return $resource('/en/quote/api/payment/:id');
});

/* istanbul ignore next  */
app.factory('Project', function ($resource) {
    return $resource('/api/project/:id', {}, {
        fields: {
            method: 'GET',
            url: '/api/project/fields'
        },
    });
});

/* istanbul ignore next  */
app.factory('ClientProjects', function ($resource) {
    return $resource('/en/api/projects?client_id=:id', {id: '@id'});
});

/* istanbul ignore next  */
app.factory('User', function ($resource) {
    return $resource('/en/api/users');
});

app.factory('glValidate', function () {
    return {
        nonEmpty: function ($data) {
            if (!$data || $data == "") {
                return "This field cannot be empty.";
            }
        },

        selected: function ($data) {
            if (!$data || $data == "") {
                return "You must choose a value.";
            }
        },

        selectedIf: function ($data, condition) {
            if (condition && (!$data || $data == "")) {
                return "You must choose a value.";
            }
        },
    };
});

app.factory('glConstants', function () {
    return {
        ClientStatus: {
            Potential: 0,
            Quoted: 1,
            ProjectUnderway: 2,
            PendingPayment: 3,
            Closed: 4,
        },
    };
});

app.factory('glAlertService', function () {
    var service = {
            add: add,
            closeAlert: closeAlert,
            closeAlertIdx: closeAlertIdx,
            clear: clear,
            get: get
        },
        alerts = [];

    return service;

    function add(type, msg) {
        alerts.push({
            type: type,
            msg: msg,
            close: function () {
                return closeAlert(this);
            }
        });

        if (alerts.length > 3) {
            closeAlertIdx(0);
        }

        return alerts;
    }

    function closeAlert(alert) {
        return closeAlertIdx(alerts.indexOf(alert));
    }

    function closeAlertIdx(index) {
        return alerts.splice(index, 1);
    }

    function clear() {
        alerts = [];
    }

    function get() {
        return alerts;
    }
});