app = angular.module('gallant.directives.glDashboardMoneySummary', [
    'tc.chartjs',
]);

app.directive('glDashboardMoneySummary', ['$window', function ($window) {
    return {
        restrict: 'A',
        scope: true,
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_dashboard_money_summary.html',
        link: function ($scope) {

            $scope.money_polar_chart_data = [
                {
                    value: 150000,
                    color: '#ffa861',
                    highlight: '#ff7300',
                    label: 'Quoted'
                },
                {
                    value: 70000,
                    color: '#b2ffaf',
                    highlight: '#00ff5f',
                    label: 'Became Clients'
                }
            ];

            // Chart.js Options
            $scope.money_polar_chart_options = {

                // Sets the chart to be responsive
                responsive: true,

                //Boolean - Show a backdrop to the scale label
                scaleShowLabelBackdrop: true,

                //String - The colour of the label backdrop
                scaleBackdropColor: 'rgba(255,255,255,0.75)',

                // Boolean - Whether the scale should begin at zero
                scaleBeginAtZero: true,

                //Number - The backdrop padding above & below the label in pixels
                scaleBackdropPaddingY: 2,

                //Number - The backdrop padding to the side of the label in pixels
                scaleBackdropPaddingX: 2,

                //Boolean - Show line for each value in the scale
                scaleShowLine: true,

                //Boolean - Stroke a line around each segment in the chart
                segmentShowStroke: true,

                //String - The colour of the stroke on each segement.
                segmentStrokeColor: '#fff',

                //Number - The width of the stroke value in pixels
                segmentStrokeWidth: 5,

                //Number - Amount of animation steps
                animationSteps: 100,

                //String - Animation easing effect.
                animationEasing: 'easeOutBounce',

                //Boolean - Whether to animate the rotation of the chart
                animateRotate: true,

                //Boolean - Whether to animate scaling the chart from the centre
                animateScale: false,

                //String - A legend template
                legendTemplate: '<ul class="tc-chart-js-legend"><% for (var i=0; i<segments.length; i++){%><li><span style="background-color:<%=segments[i].fillColor%>"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>'
            };

            $scope.money_doughnut_chart_data = [
                {
                    value: 7000,
                    color: '#ffa861',
                    highlight: '#ff7300',
                    label: "Pending Payments"
                },
                {
                    value: 3000,
                    color: "#ff0054",
                    highlight: "#FF5A5E",
                    label: "Overdue Payments"
                },
                {
                    value: 20000,
                    color: '#b2ffaf',
                    highlight: '#00ff5f',
                    label: "Paid"
                }
            ];

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

            $scope.money_bar_chart_data = {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [
                    {
                        label: 'Income in 2015',
                        fillColor: '#93f1ff',
                        strokeColor: '#93f1ff',
                        highlightFill: '#00a6ff',
                        highlightStroke: '#00a6ff',
                        data: [50000, 60000, 80000, 110000, 120000, 120000]
                    },
                    {
                        label: 'Income in 2016',
                        fillColor: '#00a6ff',
                        strokeColor: '#00a6ff',
                        highlightFill: '#93f1ff',
                        highlightStroke: '#93f1ff',
                        data: [140000, 160000, 180000, 190000, 180000, 180000]
                    }
                ]
            };

            // Chart.js Options
            $scope.money_bar_chart_options = {

                // Sets the chart to be responsive
                responsive: true,

                //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                scaleBeginAtZero: true,

                //Boolean - Whether grid lines are shown across the chart
                scaleShowGridLines: true,

                //String - Colour of the grid lines
                scaleGridLineColor: "rgba(0,0,0,.05)",

                //Number - Width of the grid lines
                scaleGridLineWidth: 0,

                //Boolean - If there is a stroke on each bar
                barShowStroke: true,

                //Number - Pixel width of the bar stroke
                barStrokeWidth: 2,

                //Number - Spacing between each of the X value sets
                barValueSpacing: 3,

                //Number - Spacing between data sets within X values
                barDatasetSpacing: 0,

                //String - A legend template
                legendTemplate: '<ul class="tc-chart-js-legend"><% for (var i=0; i<datasets.length; i++){%><li><span style="background-color:<%=datasets[i].fillColor%>"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>'
            };

        }
    };
}]);