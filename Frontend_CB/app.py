from flask import Flask
app = Flask(__name__)
 
@app.route("/")
def homepage():
    return """
<!DOCTYPE html>
<html>
<head>
<title>CancerBase</title>
<meta charset="UTF-8">
</head>
<style>
	
	
	@font-face {
		font-family: "circular-std-book";
  		src: url("/CircularStd-Medium.woff") format("woff");;
  	}

	body {
		text-align: center;
		font-size: 16pt;
		font-family: Helvetica;
	}

	.mainbox {
		text-align: center;
		width: 40%;
		margin: auto;
		height: 350px;
		margin-top: 60px;
		box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
		border-radius: 10pt;
		padding: 40px;
		font-size: 16pt;
	}

	.header {

		text-align: center;
		font-size: 25pt;
	}

	.email_signup_button {
		width: 45%;
		height: 27px;
		border-radius: 2pt;
		background-color: #2db475;
		color: white;
		padding: 9px;
		margin: auto;
	}

</style>

<body>
<script>
  // This is called with the results from from FB.getLoginStatus().
  function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
      // Logged into your app and Facebook.
      testAPI();
    } else {
      // The person is not logged into your app or we are unable to tell.
      document.getElementById('status').innerHTML = 'Please log ' +
        'into this app.';
    }
  }

  // This function is called when someone finishes with the Login
  // Button.  See the onlogin handler attached to it in the sample
  // code below.
  function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
  }

  window.fbAsyncInit = function() {
    FB.init({
      appId      : '160324368106568',
      cookie     : true,  // enable cookies to allow the server to access 
                          // the session
      xfbml      : true,  // parse social plugins on this page
      version    : 'v2.8' // use graph api version 2.8
    });

    // Now that we've initialized the JavaScript SDK, we call 
    // FB.getLoginStatus().  This function gets the state of the
    // person visiting this page and can return one of three states to
    // the callback you provide.  They can be:
    //
    // 1. Logged into your app ('connected')
    // 2. Logged into Facebook, but not your app ('not_authorized')
    // 3. Not logged into Facebook and can't tell if they are logged into
    //    your app or not.
    //
    // These three cases are handled in the callback function.

    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });

  };

  // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
      document.getElementById('status').innerHTML =
        'Thanks for logging in, ' + response.name + '!';
    });
  }
</script>
<div class="header">
<strong>Cancerbase</strong> <span style="color: #808080;">alpha</span>
</div><!--close header-->
<div class="mainbox">
<strong>Welcome to Cancerbase!</strong><br>
<span style="color: #808080; font-size: 12pt;">sign up to build your memoir and keep track of your condition</span>
<br><br><br>
<div class="fb-login-button" data-max-rows="1" data-size="large" data-button-type="continue_with" data-show-faces="false" data-auto-logout-link="false" data-use-continue-as="false"></div>


<div id="status">
</div><br>
<span style="color: #808080;">-or-</span>
<br><br>
<div class="email_signup_button"> sign up with email </div><br><br>
</div> <!--close mainbox-->
<br>
or log in 
</body>
</html>

"""

@app.route('/sign_up')
def signup():
    return "Hello World"
 
if __name__ == "__main__":
    app.run()