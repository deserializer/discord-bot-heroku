from flask import Flask, redirect, url_for, render_template
from threading import Thread

app = Flask('')

@app.route('/')
def main():
  return '''<html>

<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>johndo3</title>
	<style>@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap');

:root{
	--main-background: #0b0c0f;
	--main-fonts-color: #fff;
	--main-decor-color:#0d8a83;
    --main-header-background:#21252e;
	--main-font-family: 'Poppins', sans-serif;
}

*{
	margin: 0;
	padding: 0;
	scroll-behavior: smooth;
}

main{
	padding: 0;
	width: 100%;
	height: 100%;
	background: var(--main-background);
}

/*──────────────────
       home
──────────────────*/

#home{ 	
	margin: auto;
	height: 100vh;
	color: var(--main-fonts-color);
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: space-evenly;
}

#home .filter{
	background: url('https://images.unsplash.com/photo-1544099858-75feeb57f01b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80') no-repeat;
	background-size: cover;
	background-position:center;
    position: absolute;
    top: 0px;
    bottom: 0;
    left: 0;
    right: 0;
	opacity:.20;
}  

.intro {
	text-align:center;
    color: var(--main-fonts-color);
	z-index: 1;
	margin: auto;
	padding: 20px;
}

.intro  p{
    margin: 5px;
	font-size:1.2rem;
	font-family: var(--main-font-family);
	text-align:center;
}

 h3{
	padding-bottom: 15px;
    letter-spacing: normal;
    font-family: var(--main-font-family);
	font-style: normal;
	font-size: 60px;
	color: var(--main-fonts-color);
	text-shadow: 0px 0px 40px var(--main-decor-color);
}


/*──────────────────
    social media
──────────────────*/

.social-media{
	padding: 10px;
	display: flex;
	position: center;
    align-items: space-around;
	justify-content:center;
}

.social-media a {
    margin: 10px;
    font-size: 2rem;
    text-align:center;
    display: inline-block;
	color: var(--main-fonts-color);
}

.social-media a i{
	cursor: pointer;
}

.social-media  a:hover {
	color: var(--main-decor-color);
	text-shadow: 0 0 50px var(--main-decor-color);
}

/*────────────────── 
       footer
──────────────────*/

footer {
	width: 100%;
	height: 100%;
    background-color: var(--main-header-background);
}

.copyright {
	color: #fff;
	font-size: 1.2rem;
	line-height: 40px;
	text-align: center;
}

.copyright a{
	color: #fff;
	font-size: 1rem;
	letter-spacing: 1px;
    text-decoration: none;
}

.copyright a:hover{
	color: var(--main-decor-color);
}

/*──── hr ─────*/

hr {
    background: var(--main-decor-color);
	margin: 2px;
	height: 3px;
	width: 150px;
    border-radius:5px;
	border: hidden;
	margin-inline-start: auto;
    margin-inline-end: auto;
}

/*────────────────── 
     Scrollbar
──────────────────*/
::-webkit-Scrollbar{
    width: 5px; 
	background: rgba(5,5,5,1);
}
::-webkit-Scrollbar-thumb{
	border-radius: 10px;
	background: var(--main-decor-color);
	box-shadow: inset 0 0 20px var(--main-decor-color);
}
::-webkit-Scrollbar-track{
	margin-top: 80px;
	border-radius: 10px;
}

/*────────────────── 
     hamburger
──────────────────*/
.hamburger {
	display: none;
}

.hamburger div{
	width: 30px;
	height: 3px;
	background: #dbdbdb;
	margin: 5px;
	transition:all 0.3s ease;
}

.toggle .line1{
	transform: rotate(-45deg) translate(-5px,6px);
}

.toggle .line2{
	opacity: 0;
}

.toggle .line3{
	transform: rotate(45deg) translate(-5px,-6px);
}

@keyframes navLinkFade{
	from{
		opacity:0;
		transform: translatex(50px);
	}
	to{
		opacity: 1;
		transform:translatex(0px);
	}
}

/*────────────────── 
    media queries
──────────────────*/

@media only screen and (max-width: 1484px) and (min-width: 1214px) {
	.work{
        padding:20px 20%;
    }
}
@media only screen and (max-width: 1214px) and (min-width: 1000px) {
	.work{
        padding:20px 12%;
    }
}


@media only screen and (max-width: 500px) {

	#home, #projects, #contact{
        overflow-x: hidden;
	}
	header{
		background-color: var(--main-header-background);
	}
	.logo{
		position:absolute;
		top: 2px;
		left: 30px;
	}
	.nav-show{
		opacity: 1;
	}	 
	.nav-bar{
		position:fixed;
		top: 0px;
		right:0;
		width:60%;
		height: 100vh;
		display:flex;
		flex-direction: column;
		align-items: center;
		justify-content:space-evenly;
		background:var(--main-header-background);
		transform:translatex(100%);
		transition: transform 0.5s ease-in;
		z-index: -1;
	}
	.hamburger{
		position:absolute;
		top: 17px;
		right: 25%;
		display: block;
		cursor:pointer;
		z-index: 5;
	}	
	.nav-bar li{
		opacity:0;
	}
}

.nav-active{
	transform:translatex(0%);
}</style>
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.13.0/css/all.css">
	<link href="img/profile.png" rel="icon" type="image/png">
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js">

	</script>
	<script>
    // header scrolling effect
    $(window).on('scroll', function(){
      if($(window).scrollTop()){
          $('header').addClass('nav-show');
          
      } 
      else{
        $('header').removeClass('nav-show');
      }
        
    })

    //hamburger
    const navSlide = () => {
      const hamburger = document.querySelector(".hamburger");
      const navbar = document.querySelector(".nav-bar");
      const navLinks = document.querySelectorAll(".nav-bar li");

        hamburger.onclick = () => {
        
      navbar.classList.toggle("nav-active");
        
          //Animation links
      navLinks.forEach((link, index) => {
        if (link.style.animation) {
          link.style.animation = "";
        } else {
          link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7+1}s`;
          }
        });
        //hamburger animation
      hamburger.classList.toggle("toggle");
        }
      
      }

    window.onload = () => navSlide();
	</script>
</head>

<body>

	<div class="container">
		<!--─────────────────Home────────────────-->
	  <div id="home">
		 <div class="filter"></div>
		 <section class="intro">
		  <h3>The CarlosDiscord Project<hr></h3>
			  
		  <!--────social media links─────-->
			  <a href="https://discord.gg/6GPjN8C" target="_blank"><i class="fab fa-discord"></i></a>        
		  </div>
			 
		 </section> 
	  </div>  
	</div>

	</main>
	  <footer class="copyright">© 2020 
		  <a href="https://repl.it/@johndo3" target="_blank"> johndo3.</a>
     </footer>
	  
  </div>
  </body>
</html>'''

def run():
  app.run(host='0.0.0.0', port=8080)

def server():
  server = Thread(target=run)
  server.start()
