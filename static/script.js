/* ==========================================
   Premium Loan Approval UI
   script.js
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initializeAnimations();
    initializeForm();
    initializeInputs();
    initializeCounter();
    initializeScrollReveal();

});

/* ==========================================
   FORM
========================================== */

function initializeForm(){

    const form = document.querySelector("form");
    const button = document.querySelector(".predict-btn");

    if(!form || !button) return;

    form.addEventListener("submit",()=>{

        button.disabled = true;

        const text = button.querySelector(".btn-text");
        const loader = button.querySelector(".loader");

        if(text) text.style.display="none";

        if(loader){

            loader.style.display="inline-block";

            loader.innerHTML='<i class="fa-solid fa-spinner fa-spin"></i> Predicting...';

        }

    });

}

/* ==========================================
   INPUT EFFECTS
========================================== */

function initializeInputs(){

    const fields=document.querySelectorAll("input,select");

    fields.forEach(field=>{

        field.addEventListener("focus",()=>{

            field.parentElement.classList.add("active");

        });

        field.addEventListener("blur",()=>{

            field.parentElement.classList.remove("active");

        });

    });

}

/* ==========================================
   NUMBER FORMAT
========================================== */

document.querySelectorAll("input[type='number']").forEach(input=>{

    input.addEventListener("wheel",(e)=>{

        e.target.blur();

    });

});

/* ==========================================
   SCROLL REVEAL
========================================== */

function initializeScrollReveal(){

    const elements=document.querySelectorAll(

        ".hero,.stat-card,.form-card,.result-card"

    );

    const observer=new IntersectionObserver(entries=>{

        entries.forEach(entry=>{

            if(entry.isIntersecting){

                entry.target.classList.add("show");

            }

        });

    },{

        threshold:.15

    });

    elements.forEach(el=>{

        el.classList.add("hidden");

        observer.observe(el);

    });

}

/* ==========================================
   HERO FLOAT
========================================== */

function initializeAnimations(){

    const card=document.querySelector(".glass-card");

    if(!card) return;

    let angle=0;

    setInterval(()=>{

        angle+=0.03;

        card.style.transform=

        `translateY(${Math.sin(angle)*8}px)`;

    },30);

}

/* ==========================================
   AUTO SCROLL TO RESULT
========================================== */

window.addEventListener("load",()=>{

    const result=document.querySelector(".result");

    if(result){

        setTimeout(()=>{

            result.scrollIntoView({

                behavior:"smooth",

                block:"center"

            });

        },500);

    }

});

/* ==========================================
   COUNTER
========================================== */

function initializeCounter(){

    const stats=document.querySelectorAll(".stat-card h2");

    stats.forEach(item=>{

        if(isNaN(item.innerText)) return;

        const target=parseInt(item.innerText);

        let count=0;

        const timer=setInterval(()=>{

            count++;

            item.innerText=count;

            if(count>=target){

                clearInterval(timer);

            }

        },25);

    });

}

/* ==========================================
   RIPPLE EFFECT
========================================== */

document.querySelectorAll(".predict-btn").forEach(btn=>{

    btn.addEventListener("click",function(e){

        const circle=document.createElement("span");

        const diameter=Math.max(

            this.clientWidth,

            this.clientHeight

        );

        circle.style.width=circle.style.height=

        `${diameter}px`;

        circle.style.left=

        `${e.clientX-this.offsetLeft-diameter/2}px`;

        circle.style.top=

        `${e.clientY-this.offsetTop-diameter/2}px`;

        circle.classList.add("ripple");

        const ripple=this.getElementsByClassName("ripple")[0];

        if(ripple){

            ripple.remove();

        }

        this.appendChild(circle);

    });

});

/* ==========================================
   VALIDATION
========================================== */

const form=document.querySelector("form");

if(form){

form.addEventListener("submit",(e)=>{

const required=document.querySelectorAll("[required]");

let valid=true;

required.forEach(field=>{

if(field.value.trim()===""){

valid=false;

field.style.borderColor="#ef4444";

}

else{

field.style.borderColor="";

}

});

if(!valid){

e.preventDefault();

alert("Please complete all required fields.");

}

});

}

/* ==========================================
   SUCCESS MESSAGE ANIMATION
========================================== */

const result=document.querySelector(".result");

if(result){

result.animate([

{

opacity:0,

transform:"translateY(30px)"

},

{

opacity:1,

transform:"translateY(0)"

}

],{

duration:800,

easing:"ease"

});

}
