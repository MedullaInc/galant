app = angular.module('gallant.directives.glDashboardMoneySummary', [
    'gallant.services.glServices',
    'tc.chartjs',
]);

app.directive('glDashboardMoneySummary', ['$window', 'Payment', function ($window, Payment) {
    return {
        restrict: 'A',
        scope: true,
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_dashboard_money_summary.html',
        link: function ($scope) {

            $scope.paid = 0.0;
            $scope.overdue = 0.0;
            $scope.pending = 0.0;
            $scope.on_hold = 0.0;

            Payment.query().$promise.then(function (response) {
                angular.forEach(response, function (payment) {
                    if (payment.paid_on != null) {
                        $scope.paid += parseFloat(payment.amount.amount);
                    } else if (new Date(payment.due) < new Date()) {
                        $scope.overdue += parseFloat(payment.amount.amount);
                    } else if (new Date(payment.due) > new Date()) {
                        $scope.pending += parseFloat(payment.amount.amount);
                    } else {
                        $scope.on_hold += parseFloat(payment.amount.amount);
                    }
                });

                $scope.money_doughnut_chart_data = [
                    {
                        value: $scope.on_hold,
                        color: '#ffa861',
                        highlight: '#ff7300',
                        label: "Payments On Hold"
                    },
                    {
                        value: $scope.pending,
                        color: '#ffa861',
                        highlight: '#ff7300',
                        label: "Pending Payments"
                    },
                    {
                        value: $scope.overdue,
                        color: "#ff0054",
                        highlight: "#FF5A5E",
                        label: "Overdue Payments"
                    },
                    {
                        value: $scope.paid,
                        color: '#b2ffaf',
                        highlight: '#00ff5f',
                        label: "Paid"
                    }
                ];

            });

            // Chart.js Options
            $scope.money_doughnut_chart_options = {

                // Sets the chart to be responsive
                responsive: true,

                //Boolean - Whether we should show a stroke on each segment
                segmentShowStroke: true,

                //String - The colour of each segment stroke
                segmentStrokeColor: '#ffffff',

                //Number - The width of each segment stroke
                segmentStrokeWidth: 5,

                //Number - The percentage of the chart that we cut out of the middle
                percentageInnerCutout: 65, // This is 0 for Pie charts

                //Number - Amount of animation steps
                animationSteps: 100,

                //String - Animation easing effect
                animationEasing: 'easeOutBounce',

                //Boolean - Whether we animate the rotation of the Doughnut
                animateRotate: true,

                //Boolean - Whether we animate scaling the Doughnut from the centre
                animateScale: false,

                //String - A legend template
                legendTemplate: '<ul class="tc-chart-js-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'

            };

        }
    };
}]);