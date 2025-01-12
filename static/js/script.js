const link = document.body;
link.addEventListener("click",(e)=>{
    if(e.target.tagName=="IMG"){
        text = e.target.previousElementSibling.innerText;
        navigator.clipboard.writeText(text);
        e.target.nextElementSibling.style.opacity=1;
        setTimeout(()=>{
            e.target.nextElementSibling.style.opacity=0; 
        },3000)
    }
})