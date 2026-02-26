docuement.addEventListener("DOMContentLoaded" , function(){
    tinymce.init({
        selector:"textarea",
        height : 400 , 
        menubar : true ,
        plugins:"lists link image table code ",
        toolbar: "undo redo | formatselect | bold italic |alignment aligncenter alignright | bullist numlist | code " 

    });
});