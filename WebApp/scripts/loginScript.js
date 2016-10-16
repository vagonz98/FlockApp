var http = new XMLHttpRequest();
var url = "riceflock.com/signin";

// var params = "lorem=ipsum&name=binny";
// http.open("POST", url, true);

//Send the proper header information along with the request
http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

// http.onreadystatechange = function() {//Call a function when the state changes.
//     if(http.readyState == 4 && http.status == 200) {
//         alert(http.responseText);
//     }
// }

// http.send(username);

function sendLoginInfo() {
	var username = document.getElementById("user").value;
	var password = document.getElementById("pd").value;

	http.send("username=" + username + "&password=" + password);

}