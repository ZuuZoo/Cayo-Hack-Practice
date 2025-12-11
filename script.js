var randomNumber = random8();
var s1randomNumber = random8();
var s2randomNumber = random8();
var s3randomNumber = random8();
var s4randomNumber = random8();
var s5randomNumber = random8();
var s6randomNumber = random8();
var s7randomNumber = random8();
var s8randomNumber = random8();

   const sNums = {
    1: s1randomNumber,
    2: s2randomNumber,
    3: s3randomNumber,
    4: s4randomNumber,
    5: s5randomNumber,
    6: s6randomNumber,
    7: s7randomNumber,
    8: s8randomNumber
};

function loaded() {
    active = 1
    console.log("Page loaded");
    document.getElementById("main_finger").src = "pelda" + randomNumber + ".png";
    console.log("Image set to pelda" + randomNumber + ".png");

    for (let i = 1; i <= 8; i++) {
        document.getElementById("sor" + i + "_image").src = "pelda" + randomNumber + "/" + sNums[i] + ".png";
    }
}

function random8() {
    return Math.floor(Math.random() * 8) + 1;
}

document.onkeydown = function(event) {
         switch (event.keyCode) {


            case 37:
               if (document.getElementById("sor" + active + "_image").classList.contains("active")) {

                /* 🔥 dinamikusan csökkentjük az sNums[active] értéket */
                sNums[active]--;

                if (sNums[active] < 1) {
                    sNums[active] = 8;
                }

                document.getElementById("sor" + active + "_image").src =
                    "pelda" + randomNumber + "/" + sNums[active] + ".png";
                }

            break;


            case 38:
                document.getElementById("sor" + active + "_image").classList.remove("active")
                active--;
                if (active < 1) {
                    active = 8;
                }
                document.getElementById("sor" + active + "_image").classList.add("active")
                helyy=document.getElementById("sor" + active + "_image").offsetTop;
                document.getElementById("selector_frame_image").style.top = helyy + "px";
            break;


            case 39:
               if (document.getElementById("sor" + active + "_image").classList.contains("active")) {

                sNums[active]++;

                if (sNums[active] > 8) {
                    sNums[active] = 1;
                }

                document.getElementById("sor" + active + "_image").src =
                    "pelda" + randomNumber + "/" + sNums[active] + ".png";
                }

            break;


            case 40:
                document.getElementById("sor" + active + "_image").classList.remove("active")
                active++;
                if (active > 8) {
                    active = 1;
                }
                document.getElementById("sor" + active + "_image").classList.add("active")
                helyy=document.getElementById("sor" + active + "_image").offsetTop;
                document.getElementById("selector_frame_image").style.top = helyy + "px";
            break;
         }
         setTimeout(check, 0);
      };



/*document.getElementById("sor1_image").classList.remove("active")*/

function check() {
    let allCorrect = true; // kezdetben feltételezzük, hogy minden jó

    for (let i = 1; i <= 8; i++) {
        const elem = document.getElementById("sor" + i + "_image");

        // .endsWith a teljes URL-re is működik
        if (!elem.src.endsWith("pelda" + randomNumber + "/" + i + ".png")) {
            allCorrect = false; // ha bármi nem stimmel, false
            break; // nincs értelme tovább ellenőrizni
        }
    }

    if (allCorrect) {
        alert("Minden sor helyes!");
    }
}