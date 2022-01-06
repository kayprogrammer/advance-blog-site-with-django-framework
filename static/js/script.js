$(document).ready(function() {

    
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-post .modal-content").html("");
                $("#modal-post").modal("show");
            },
            success: function (data) {

                $("#modal-post .modal-content").html(data.html_form);
            }
        });
    };

    var loadForm2 = function () {
      var btn = $(this);
      $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
              $("#modal-post2 .modal-content").html("");
              $("#modal-post2").modal("show");
          },
          success: function (data) {

              $("#modal-post2 .modal-content").html(data.html_form);
          }
      });
    };

    var loadForm3 = function () {
      var btn = $(this);
      $.ajax({
          url: btn.attr("data-url"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
              $("#modal-post3 .modal-content").html("");
              $("#modal-post3").modal("show");
          },
          success: function (data) {

              $("#modal-post3 .modal-content").html(data.html_form);
          }
      });
    };

    var saveForm = function () {
        var form = $(this);
        var fd = new FormData(this);

        $.ajax({
          url: form.attr("action"),
          data: fd,
          type: form.attr("method"),
          dataType: 'json',
          enctype: 'multipart/form-data',
          contentType:false,
          processData: false,
          cache: false, 
          beforeSend: function(){
            $('.clearfix').show()
          },
          success: function (data) {
            if (data.form_is_valid) {
              Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Post has been added',
                button :'Ok',
                timer : 2500,
              });
              $("#post-table").html(data.html_post_list);
              $("#modal-post").modal("hide");
            }

            else {
              $("#modal-post .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      };

      var saveForm3 = function () {
        var form = $(this);
        var fd = new FormData(this);

        $.ajax({
          url: form.attr("action"),
          data: fd,
          type: form.attr("method"),
          dataType: 'json',
          enctype: 'multipart/form-data',
          contentType:false,
          processData: false,
          cache: false,
          beforeSend: function(){
            $('.clearfix').show()
          },
          success: function (data) {
            if (data.form_is_valid) {
              Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Post has been added',
                button :'Ok',
                timer : 2500,
              });
              $("#post-table3").html(data.html_post_list3);
              $("#modal-post3").modal("hide");
            }

            else {
              $("#modal-post3 .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      };

    var updateForm = function () {
      var form = $(this);
      var fd = new FormData(this);

      $.ajax({
        url: form.attr("action"),
        data: fd,
        type: form.attr("method"),
        dataType: 'json',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        beforeSend: function(){
          $('.clearfix').show()
        },
        success: function (data) {
          if (data.form_is_valid) {
            Swal.fire({
              icon: 'success',
              title: 'Success',
              text: 'Post has been updated',
              button :'Ok',
              timer : 2500,
            });
            $("#post-table").html(data.html_post_list);
            $("#modal-post").modal("hide");
          }

          else {
            $("#modal-post .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };

    var updateForm2 = function () {
      var form = $(this);
      var fd = new FormData(this);

      $.ajax({
        url: form.attr("action"),
        data: fd,
        type: form.attr("method"),
        dataType: 'json',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        beforeSend: function(){
          $('.clearfix').show()
        },
        success: function (data) {
          if (data.form_is_valid) {
            Swal.fire({
              icon: 'success',
              title: 'Success',
              text: 'Post has been updated',
              button :'Ok',
              timer : 2500,
            });
            $("#post-table2").html(data.html_post_list2);
            $("#modal-post2").modal("hide");
          }

          else {
            $("#modal-post2 .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };

    var updateForm3 = function () {
      var form = $(this);
      var fd = new FormData(this);

      $.ajax({
        url: form.attr("action"),
        data: fd,
        type: form.attr("method"),
        dataType: 'json',
        enctype: 'multipart/form-data',
        processData: false,
        contentType: false,
        cache: false,
        beforeSend: function(){
          $('.clearfix').show()
        },
        success: function (data) {
          if (data.form_is_valid) {
            Swal.fire({
              icon: 'success',
              title: 'Success',
              text: 'Post has been updated',
              button :'Ok',
              timer : 2500,
            });
            $("#post-table3").html(data.html_post_list3);
            $("#modal-post3").modal("hide");
          }

          else {
            $("#modal-post3 .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };

    var delForm = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        beforeSend: function(){
          $('.clearfix').show()
        },
        success: function (data) {
          data.preventDefault;
          if (data.form_is_valid) {
            Swal.fire({
              icon: 'success',
              title: 'Success',
              text: 'Article has been deleted',
              button :'Ok',
              timer : 2500
            }).then(function(){
              window.location.href = "/"
            });
            $("#post-table").html(data.html_post_list);
            $("#modal-post").modal("hide");
          }

          else {
            $("#modal-post .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };


    /* Binding */
    $(".js-create-post").click(loadForm);
    $(".js-create-post3").click(loadForm3);
    $("#modal-post").on("submit", ".js-post-create-form", saveForm);
    $("#modal-post3").on("submit", ".js-post-create-form", saveForm3);

    // Update post
    $("#post-table").on("click", ".js-update-post", loadForm);
    $("#post-table2").on("click", ".js-update-post2", loadForm2);
    $("#post-table3").on("click", ".js-update-post3", loadForm3);
    $("#modal-post").on("submit", ".js-post-update-form", updateForm);
    $("#modal-post2").on("submit", ".js-post-update-form", updateForm2);
    $("#modal-post3").on("submit", ".js-post-update-form", updateForm3);
    // Delete post
    $(".js-delete-post").click(loadForm);
    $("#modal-post").on("submit", ".js-post-delete-form", delForm);
});
