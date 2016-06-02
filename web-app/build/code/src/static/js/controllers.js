
var app = angular.module('directoryApp.controllers',[]);
app.controller("users", function($scope,  $http, $routeParams, $route,$window){
    $scope.role_name = $window.role_name;
    $http.get("http://localhost:5000/users").success(function(response){
	$scope.users = response;
    });

    });
app.controller("view-user", function($scope,  $http, $routeParams, $route,$window){
    $scope.role_name = $window.role_name;
    $scope.session_email=$window.session_email;
    $http.get("http://localhost:5000/users/"+$routeParams.id).success(function(response){
      console.log(response);
       	$scope.user = response;
    });
    $scope.delete_user=function(){
    
    $http.delete("http://localhost:5000/users/"+$routeParams.id, {headers:{'session' : $scope.session_email}}).success(function(response){
    	alert("deleted user");
      console.log(response);
      window.history.back();
    });
  
   }; 
});
app.controller("add-user", function($scope,   $http,  $routeParams,  $route,$window){
    $scope.role_name=$window.role_name;
    $scope.session_email=$window.session_email;
    $scope.myText="you haven't clicked submit yet"
    $scope.add_user=function(){
       
       var data={
            name:$scope.name,
            email:$scope.email,
            role_id:$scope.role,
            session: $scope.session_email
            };

            
            $http.post("http://localhost:5000/users",data).success(function(reponse){
            $scope.PostDataResponse = data;
            $scope.myText="You added successfully"
            window.history.back();
            }).error(function(response) {
            $scope.ResponseDetails ="Data:" +data+
            "<hr />status: " + status +
            "<hr />headers: " + header +
            "<hr />config: " + config;
            });


};
});
app.controller("edit-user", function($scope,   $http,  $routeParams,  $route,$window){
    $scope.role_name=$window.role_name;
    $scope.session_email=$window.session_email;
    $scope.myText="you haven't clicked submit yet"
    $scope.edit_user=function(){
       
       var data={
            name:$scope.name,
            email:$scope.email,
            role_id:$scope.role,
            session: $scope.session_email
            };
            
            $http.put("http://localhost:5000/users/"+$routeParams.id,data).success(function(response){
            alert("updated successfully");
            $scope.PostDataResponse = data;
            $scope.myText="Edited details successfully"
            }).error(function(response) {
            alert("Unable to update");
            $scope.ResponseDetails ="Data:" +data+
            "<hr />status: " + status +
            "<hr />headers: " + header +
            "<hr />config: " + config;
            });


};
});
