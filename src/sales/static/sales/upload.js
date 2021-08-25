const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const alertbox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

Dropzone.autoDiscover =false
const myDropzone = new Dropzone('#my-dropzone',{
    url:'/upload/',
    init: function(){
        this.on('sending', function(file,xhr,formData){
            console.log('sending')  
            formData.append('csrfmiddlewaretoken',csrf)
        })
        this.on('success', function(file, response){
            console.log(response)
            const ex = response.ex
            if(ex){
                handleAlerts('danger','File already exist')

            }else {
                handleAlerts('success','File uploaded successfully')
            }
        })
    },
    maxFiles:3,
    maxFilesize:3,
    acceptedFiles:'.csv'
})
    
