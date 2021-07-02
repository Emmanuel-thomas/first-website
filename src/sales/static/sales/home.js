console.log('hello world');

const reportBtn = document.getElementById('report-btn');
const img =document.getElementById('img');
const modalBody =document.getElementById('modal-body');

const reportName =document.getElementById('id_name')
const reportRemarks=document.getElementById('id_remarks')
const csrf =document.getElementsByName('csrfmiddlewaretoken')
console.log(csrf)



 console.log("hii friende")
console.log(reportBtn);
console.log(img);
if (img){
    console.log("i am inside ")
    reportBtn.classList.remove('not-visible');
}

reportBtn.addEventListener('click', ()=>{
    console.log('clickedwe');
    img.setAttribute('class','w-100');
    modalBody.prepend(img);
})