
function downloadEncodedImage() {
    window.open('/static/images/encoded_image.png', '_blank');
}

const title = document.querySelector(".title")

function typeEffect(element, text) {
    let i = 0;
  
    function type() {
      if (i < text.length) {
        element.innerHTML += text.charAt(i);
        i++;
        setTimeout(type, 50); 
      }
    }
  
    type();
  }
  
typeEffect(title, "Steganography");

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
const h2s = document.querySelectorAll("h2");

let interval = null;

h2s.forEach((h2) => {
    h2.onmouseover = event => {
        
        let iteration = 0;
  
        clearInterval(interval);
  
        interval = setInterval(() => {
        event.target.innerText = event.target.innerText
            .split("")
            .map((letter, index) => {
        if(index < iteration) {
            return event.target.dataset.value[index];
        }
      
        return letters[Math.floor(Math.random() * 52)]
        })
        .join("");
    
        if(iteration >= event.target.dataset.value.length){ 
            clearInterval(interval);
        }
    
        iteration += 1 / 3;
        }, 40);
    }
});

function validateEncode() {
    const image = document.querySelector("form[action = '/encode'] input[name='image']");
    if(image.files.length === 0) {
        alert( "Please select an image")
        return false;
    }
}

function validateDecode() {
    const image = document.querySelector("form[action = '/decode'] input[name='image']");
    if(image.files.length === 0) {
        alert( "Please select an image")
        return false;
    }
}
