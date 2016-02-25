app = angular.module('quotes.directives.qtSectionTable', [
    'quotes.services.qtServices',
    ]);

app.directive('qtSectionTable', ['Section', function (Section) {
        return {
            restrict: 'A',
            scope: true,
            controller: ['$scope','Section',
                function ($scope, Section) {
                    $scope.isCollapsed = false;
                }
            ],
            templateUrl: '/static/quotes/html/qt_quote_section_table.html',
            link: function ($scope) {
                
                
                
                $scope.showSection = function (section){
                    if($scope.idType == "token"){
                        id = section.id;
                        section.views = section.views+1;
                        Section.update({id: id, user: $scope.quote.user}, section);    
                    }                   
                }

                $scope.removeSection = function (index) {
                    $scope.quote.sections.splice(index, 1);
                };

            }
        };
    }]);