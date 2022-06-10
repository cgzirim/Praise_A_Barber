var jwt = localStorage.getItem("jwt");
console.log('here');
if (jwt == null) {
  window.location.href = './login.html'
}

function loadUser() {
    // var jwt = localStorage.getItem("jwt");
    // console.log('here');
  const xhttp = new XMLHttpRequest();
  xhttp.open("GET", "http://praiseabarber.herokuapp.com/api/v1/dashboard");
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.setRequestHeader("x-access-token", jwt);
  xhttp.send();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      const objects = JSON.parse(this.responseText);
      if (objects["status"] == "ok") {
        const user = objects["user"]
        document.getElementById("email").innerHTML = user["email"];
        document.getElementById("profile_img_url").src = user["profile_img_url"];
        document.getElementById("username").innerHTML = user["username"];
        document.getElementById("city").innerHTML = user["city"];
        document.getElementById("rating").innerHTML = user["rating"];

      }
    }
  };
}

loadUser();

function logout() {
  localStorage.removeItem("jwt");
  window.location.href = './login.html'
}
