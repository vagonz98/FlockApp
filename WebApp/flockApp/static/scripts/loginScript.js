window.onload = function() {
	document.getElementById("login").onclick = function fun() {
		sendLoginInfo();
	}
}
var baseURL = ""
// var params = "lorem=ipsum&name=binny";
// http.open("POST", url, true);


// http.onreadystatechange = function() {//Call a function when the state changes.
//     if(http.readyState == 4 && http.status == 200) {
//         alert(http.responseText);
//     }
// }

// http.send(username);

function sendLoginInfo() {
	var http = new XMLHttpRequest();
	var url = "/login";
	var data = new FormData();
	var username = document.getElementById("user").value;
	var password = document.getElementById("pw").value;
	data.append('username', username);
	data.append('password', password);
	http.open("POST", url, true);
	http.onreadystatechange = function() {//Call a function when the state changes.
       if(http.readyState == 4 && http.status == 200) {
           window.location = http.responseText;
       }
    }
	http.send(data);

}