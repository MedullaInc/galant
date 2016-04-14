app = angular.module('gallant.services.glServices', ['ngResource']);

/* istanbul ignore next */
app.factory('Client', function ($resource) {
    return $resource('/api/client/:id', {}, {
        fields: {
            method: 'GET',
            url: '/api/client/fields'
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
        return alerts.push({
            type: type,
            msg: msg,
            close: function () {
                return closeAlert(this);
            }
        });
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