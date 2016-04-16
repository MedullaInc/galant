app = angular.module('gallant.directives.glDashboardWorkSummary', [
    'tc.chartjs',
]);

app.directive('glDashboardWorkSummary', ['$window', function ($window) {
    return {
        restrict: 'A',
        scope: true,
        controller: ['$scope', function ($scope) {
        }],
        templateUrl: '/static/gallant/html/gl_dashboard_work_summary.html',
        link: function ($scope) {

            $scope.work_polar_chart_data = [
                {
                    value: 20,
                    color: "#02deff",
                    highlight: "#93f1ff",
                    label: 'Approached People'
                },
                {
                    value: 15,
                    color: '#FDB45C',
                    highlight: '#FFC870',
                    label: 'Quoted People'
                },
                {
                    value: 7,
                    color: '#00ff5f',
                    highlight: '#FFC870',
                    label: 'Became Clients'
                }
            ];

            // Chart.js Options
            $scope.work_polar_chart_options = {

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

            $scope.work_doughnut_chart_data = [
                {
                    value: 10,
                    color: "#02deff",
                    highlight: "#93f1ff",
                    label: "Active Serivces"
                },
                {
                    value: 1,
                    color: "#ff022c",
                    highlight: "#FF5A5E",
                    label: "Overdue Services"
                },
                {
                    value: 20,
                    color: '#00ff5f',
                    highlight: '#FFC870',
                    label: "Completed Services"
                }
            ];

            // Chart.js Options
            $scope.work_doughnut_chart_options = {

                // Sets the chart to be responsive
                responsive: true,

                //Boolean - Whether we should show a stroke on each segment
                segmentShowStroke: true,

                //String - The colour of each segment stroke
                segmentStrokeColor: '#ffffff',

                //Number - The width of each segment stroke
                segmentStrokeWidth: 5,

                //Number - The percentage of the chart that we cut out of the middle
                percentageInnerCutout: 70, // This is 0 for Pie charts

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

            $scope.work_bar_chart_data = {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [
                    {
                        label: 'Projects in 2015',
                        fillColor: '#02deff',
                        strokeColor: '#02deff',
                        highlightFill: '#02deff',
                        highlightStroke: '#02deff',
                        data: [5, 6, 8, 11, 12, 12]
                    },
                    {
                        label: 'Projects in 2016',
                        fillColor: '#00ff00',
                        strokeColor: '#00ff00',
                        highlightFill: '#00ff00',
                        highlightStroke: '#00ff00',
                        data: [14, 16, 18, 19, 18, 18]
                    }
                ]
            };

            // Chart.js Options
            $scope.work_bar_chart_options = {

                // Sets the chart to be responsive
                responsive: true,

                //Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
                scaleBeginAtZero: true,

                //Boolean - Whether grid lines are shown across the chart
                scaleShowGridLines: true,

                //String - Colour of the grid lines
                scaleGridLineColor: "rgba(0,0,0,.05)",

                //Number - Width of the grid lines
                scaleGridLineWidth: 1,

                //Boolean - If there is a stroke on each bar
                barShowStroke: true,

                //Number - Pixel width of the bar stroke
                barStrokeWidth: 1,

                //Number - Spacing between each of the X value sets
                barValueSpacing: 3,

                //Number - Spacing between data sets within X values
                barDatasetSpacing: 3,

                //String - A legend template
                legendTemplate: '<ul class="tc-chart-js-legend"><% for (var i=0; i<datasets.length; i++){%><li><span style="background-color:<%=datasets[i].fillColor%>"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>'
            };

        }
    };
}]);