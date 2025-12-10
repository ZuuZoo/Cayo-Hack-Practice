function loaded() {
    console.log("Page loaded");
    var randomNumber = Math.floor(Math.random() * 8) + 1;
    document.getElementById("main_finger").src = "pelda" + randomNumber + ".png";
    console.log("Image set to pelda" + randomNumber + ".png");
}