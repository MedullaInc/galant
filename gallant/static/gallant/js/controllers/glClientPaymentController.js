app = angular.module('gallant.controllers.glClientPaymentController', ['gallant.services.glServices']);

app.controller('glClientPaymentController', ['$scope', '$attrs', '$uibModal', '$log', 'ClientQuote', '$http', '$window', 'Payment', function ($scope, $attrs, $uibModal, $log, ClientQuote, $http, $window, Payment) {

    Payment.query({client_id: $attrs.clientId}).$promise.then(function (response) {
        $scope.payments = response;
    });

    $scope.openEditModal = function (payment_id) {
        $uibModal.open({
            templateUrl: '/static/gallant/html/gl_client_payment_modal.html',
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope, $uibModalInstance, ClientQuote, createPayment, updatePayment, Payment, Client) {

                // When form loads, it will load quotes
                $scope.quotes = [];

                $scope.getQuotes = function () {
                    ClientQuote.query({client_id: $attrs.clientId}).$promise.then(function (response) {
                        $scope.quotes = response;
                    });
                };

                $scope.hasServices = function (quote) {
                    return quote.status == 5 && quote.projects.length > 0;
                };
                // Load default payment formant & due date
                if (typeof payment_id !== 'undefined') {
                    Payment.get({id: payment_id}).$promise.then(function (response) {
                        $scope.payment = response;
                        $scope.currency = '( in ' + response.amount.currency + ' )';
                        if ($scope.payment.due) {
                            $scope.payment.due = new Date($scope.payment.due);
                        } else {
                            $scope.payment.due = new Date();
                        }
                        if ($scope.payment.paid_on) {
                            $scope.payment.paid_on = new Date($scope.payment.paid_on);
                        }
                    });
                } else {
                    $scope.payment = {amount: {currency: '', amount: null}};
                    $scope.payment.due = new Date();
                }

                $scope.getQuotes();

                // When selecting a quote, currency will update as well as quote
                $scope.updateCurrency = function (quote_id) {
                    var quote = $scope.quotes.find(function (q) { return q.id == quote_id; });

                    Client.get({id: quote.client}).$promise.then(function (response) {
                       if (response.currency) {
                        $scope.currency = '( in ' + response.currency + ' )';
                       } else {
                        $scope.currency = '( N/A )'
                       }
                    });

                };

                // Date pickers
                $scope.openDueDatePicker = function () {
                    $scope.due_date_opened = true;
                };

                $scope.openPaidDatePicker = function () {
                    $scope.paid_date_opened = true;
                };

                // Form functions
                $scope.createPayment = createPayment;
                $scope.updatePayment = updatePayment;
                $scope.submit = function () {
                    if (typeof $scope.payment == 'undefined' || typeof $scope.payment.quote == 'undefined' || typeof $scope.payment.amount.amount == 'undefined' || $scope.payment.amount.amount <= 0.0 || typeof $scope.payment.description == 'undefined') {
                        $scope.errors = "Quote, Amount & Description are required!";
                    } else {
                        $scope.errors = "";
                        // TODO: Change form to ng-model='amount.amount'
                        if ($scope.payment.id) {
                            $scope.updatePayment($scope.payment);
                        } else {
                            $scope.createPayment($scope.payment);
                        }

                        $uibModalInstance.dismiss('close');

                    }
                };

                // Modal functions
                $scope.cancel = function () {
                    $uibModalInstance.dismiss('cancel');
                };
            },
            resolve: {

                createPayment: /* istanbul ignore next */ function () {
                    return $scope.createPayment;
                },
                updatePayment: /* istanbul ignore next */ function () {
                    return $scope.updatePayment;
                },
            }
        });
    };

    $scope.createPayment = function (payment) {

        var newPayment = {
            quote_id: payment.quote,
            amount: payment.amount,
            description: payment.description,
            due: payment.due,
            paid_on: payment.paid_on,
            notes: []
        };

        newPayment.amount.amount = parseFloat(payment.amount.amount);

        var new_payment = Payment.save(newPayment);
        $scope.payments.push(new_payment);

    };

    $scope.updatePayment = function (payment) {

        var updated_payment = $scope.payments.find(
            function (a) {
                if (a.id == payment.id) {
                    return a
                }
            });

        $scope.payments.splice($scope.payments.indexOf(updated_payment), 1);
        Payment.update({id: payment.id}, payment, function (response) {
            $scope.payments.push(payment);
        });
    };

}]);