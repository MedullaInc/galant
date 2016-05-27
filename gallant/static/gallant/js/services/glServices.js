app = angular.module('gallant.services.glServices', ['ngResource']);

/* istanbul ignore next */
app.factory('Client', ['$resource', function ($resource) {
    return $resource('/api/client/:id', {}, {
        fields: {
            method: 'GET',
            url: '/api/client/fields'
        },
    });
}]);

/* istanbul ignore next */
app.factory('ClientQuote', ['$resource', function ($resource) {
    return $resource('/en/quote/api/quote/:id');
}]);

/* istanbul ignore next */
app.factory('Payment', ['$resource', function ($resource) {
    return $resource('/en/quote/api/payment/:id');
}]);


/* istanbul ignore next */
app.factory('Service', ['$resource', function ($resource) {
    return $resource('/api/service/:id');
}]);

/* istanbul ignore next  */
app.factory('Project', ['$resource', function ($resource) {
    return $resource('/api/project/:id', {}, {
        fields: {
            method: 'GET',
            url: '/api/project/fields'
        },
    });
}]);

/* istanbul ignore next  */
app.factory('User', ['$resource', function ($resource) {
    return $resource('/en/api/users');
}]);

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

/* istanbul ignore next */
app.factory('glConstants', function () {
    return {
        ClientStatus: {
            Potential: 0,
            Quoted: 1,
            ProjectUnderway: 2,
            PendingPayment: 3,
            Closed: 4,
        },
        ServiceStatus: {
            OnHold: 0,
            PendingAssignment: 1,
            Active: 2,
            Overdue: 3,
            Completed: 4,
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

        if (alerts.length > 1) {
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