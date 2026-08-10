import streamlit.components.v1 as components


def show_vanta():

    components.html(
        """
<!DOCTYPE html>
<html>

<head>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>

<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.net.min.js"></script>

<style>

html,
body{

margin:0;

overflow:hidden;

height:100%;

}

#vanta{

position:fixed;

top:0;

left:0;

width:100vw;

height:100vh;

z-index:-999;

}

</style>

</head>

<body>

<div id="vanta"></div>

<script>

VANTA.NET({

el:"#vanta",

mouseControls:true,

touchControls:true,

gyroControls:false,

minHeight:200,

minWidth:200,

scale:1,

scaleMobile:1,

color:0x22d3ee,

backgroundColor:0x071a2e,

points:9,

maxDistance:18,

spacing:18,

showDots:true

});

</script>

</body>

</html>
        """,
        height=0,
    )