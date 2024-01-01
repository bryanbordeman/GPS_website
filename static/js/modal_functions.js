$(function () {
    
    // Read and Delete modal buttons open modal with id="modal"
     // The formURL is retrieved from the data of the element
     $(".bs-modal").each(function () {
       $(this).modalForm({formURL: $(this).data("form-url")});
   });

   // Hide message
   $(".alert").fadeTo(2000, 500).slideUp(500, function () {
       $(".alert").slideUp(500);
   });
});


