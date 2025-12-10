
var randomNumber = random8();


function loaded() {
    active = 1
    console.log("Page loaded");
    document.getElementById("main_finger").src = "pelda" + randomNumber + ".png";
    console.log("Image set to pelda" + randomNumber + ".png");

    document.getElementById("sor1_image").src = "pelda" +randomNumber +"/"+random8()+".png"
    document.getElementById("sor2_image").src = "pelda" +randomNumber +"/"+random8()+".png"
    document.getElementById("sor3_image").src = "pelda" +randomNumber +"/"+random8()+".png"
    document.getElementById("sor4_image").src = "pelda" +randomNumber +"/"+random8()+".png"
    document.getElementById("sor5_image").src = "pelda" +randomNumber +"/"+random8()+".png"
    document.getElementById("sor6_image").src = "pelda" +randomNumber +"/"+random8()+".png"
    document.getElementById("sor7_image").src = "pelda" +randomNumber +"/"+random8()+".png"
    document.getElementById("sor8_image").src = "pelda" +randomNumber +"/"+random8()+".png"
}
function random8() {
    return Math.floor(Math.random() * 8) + 1;
}




/*document.getElementById("sor1_image").classList.remove("active")*/
