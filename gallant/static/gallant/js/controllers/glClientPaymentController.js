app = angular.module('gallant.controllers.glClientPaymentController', ['gallant.services.glServices']);

app.controller('glClientPaymentController', ['$scope', '$attrs', '$uibModal', '$log', 'Quote', '$http', '$window', 'Payment', function ($scope, $attrs, $uibModal, $log, Quote, $http, $window, Payment) {

    Payment.query({client_id: $attrs.clientId}).$promise.then(function (response) {
        $scope.payments = response;
    });

    $scope.openEditModal = function (payment_id) {
        $uibModal.open({
            templateUrl: '/static/gallant/html/gl_client_payment_modal.html',
            backdrop: true,
            windowClass: 'modal',
            controller: function ($scope, $uibModalInstance, Quote, createPayment, Payment) {

                // When form loads, it will load quotes
                $scope.quotes = [];

                $scope.getQuotes = function () {
                    Quote.query({client_id: $attrs.clientId}).$promise.then(function (response) {
                        $scope.quotes = response;
                    });
                };

                $scope.hasServices = function (quote) {
                    return quote.services.length > 0 && quote.status == 5;
                };
                // Load default payment formant & due date
                if (payment_id) {
                    Payment.get({id: payment_id}).$promise.then(function (response) {
                        $scope.payment = response;
                    });
                } else {
                    $scope.payment = {amount: {currency: '', amount: null}};
                    $scope.payment.due = new Date();
                }

                $scope.getQuotes();

                // When selecting a quote, currency will update as well as quote
                $scope.updateCurrency = function (quote_id) {
                    $scope.payment.amount.currency = $.grep($scope.quotes, function (e) {
                        return e.id == quote_id
                    })[0].services[0].cost.currency;
                    $scope.currency = '( in ' + $.grep($scope.quotes, function (e) {
                            return e.id == quote_id
                        })[0].services[0].cost.currency + ' )';
                    if ($scope.currency == '( in  )') {
                        $scope.currency = '( N/A )'
                    }
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
                $scope.submit = function () {
                    if (typeof $scope.payment == 'undefined' || typeof $scope.payment.quote_id == 'undefined' || typeof $scope.payment.amount.amount == 'undefined' || $scope.payment.amount.amount <= 0.0 || typeof $scope.payment.description == 'undefined' ) {
                        $scope.errors = "Quote, Amount & Description are required!";
                    } else {
                        $scope.errors = "";
                        // TODO: Change form to ng-model='amount.amount'
                        $scope.createPayment($scope.payment);
                        $uibModalInstance.dismiss('close');
                    }
                };

                // Modal functions
                $scope.cancel = function () {
                    $uibModalInstance.dismiss('cancel');
                };
            },
            resolve: {
                createPayment: function () {
                    return $scope.createPayment;
                },
            }
        });
    };

    $scope.createPayment = function (payment) {
        var newPayment = {
            quote_id: payment.quote_id,
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

}]);