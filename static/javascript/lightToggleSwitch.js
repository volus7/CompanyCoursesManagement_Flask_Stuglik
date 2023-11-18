const lightToggle = document.getElementById('checkboxInput')
const ligths = document.getElementById("content")
lightToggle.addEventListener('change', () => {
    if(lightToggle.checked){
        ligths.style.color = "var(--white)"
    }
    else{
        ligths.style.color = "var(--bg)"
    }
})