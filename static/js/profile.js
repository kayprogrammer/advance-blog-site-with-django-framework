$(document).ready(function() {
  
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function (e) {
                $("#modal-profile .modal-content").html("");
                $("#modal-profile").modal("show");
            },
            success: function (data) {

                $("#modal-profile .modal-content").html(data.html_form);
                
            }
        });
    };

    $('#file').on('change', function(){
      const url = URL.createObjectURL($('#file').files[0])
      $('#img-box').html(`<img src="${url}" width="250" height="282">`)
    })

    var saveForm = function () {
        var form = $(this);
        var fd = new FormData(this);

        $.ajax({
          url: form.attr("action"),
          data: fd,
          type: form.attr("method"),
          dataType: 'json',
          enctype: 'multipart/form-data',
          contentType: false,
          processData: false,
          cache: false,
          success: function (data) {
            
            if (data.form_is_valid) {
              Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Profile has been successfully updated',
                button :'Ok',
                timer : 2500,
              });
              $("#profile").html(data.html_profile_list);
              $("#modal-profile").modal("hide");
            }

            else {
              $("#modal-profile .modal-content").html(data.html_form);
            }
          }
        });
        return false;
    };

    /* Binding */
    $(".js-update-profile").click(loadForm);
    $("#modal-profile").on("submit", ".js-profile-update-form", saveForm);

});