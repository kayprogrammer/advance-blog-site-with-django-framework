$(document).ready(function() {

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-news .modal-content").html("");
                $("#modal-news").modal("show");
            },
            success: function (data) {

                $("#modal-news .modal-content").html(data.html_form);
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
                $("#modal-news2 .modal-content").html("");
                $("#modal-news2").modal("show");
            },
            success: function (data) {

                $("#modal-news2 .modal-content").html(data.html_form);
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
                text: 'News article has been added',
                button :'Ok',
                timer : 2500,
              });
              $("#news-table").html(data.html_news_list);
              $("#modal-news").modal("hide");
            }

            else {
              $("#modal-news .modal-content").html(data.html_form);
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
                text: 'News article has been updated',
                button :'Ok',
                timer : 2500,
              });
              $("#news-table").html(data.n_obj_list);
              $("#modal-news").modal("hide");
            }
  
            else {
              $("#modal-news .modal-content").html(data.html_form);
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
                text: 'News article has been deleted',
                button :'Ok',
                timer : 2500
              }).then(function(){
                window.location.href = newspage_url
              });
              $("#modal-news2").modal("hide");
            }
  
            else {
              $("#modal-news2 .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      };

    /* Binding */
    $(".js-create-news").click(loadForm);
    $("#modal-news").on("submit", ".js-news-create-form", saveForm);

    // Update post
    $("#news-table").on("click", ".js-update-news", loadForm);
    $("#modal-news").on("submit", ".js-news-update-form", updateForm);
    // Delete post
    $(".js-delete-news").click(loadForm2);
    $("#modal-news2").on("submit", ".js-news-delete-form", delForm);

})
