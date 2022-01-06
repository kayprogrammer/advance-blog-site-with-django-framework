$(document).ready(function() {
    
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-question .modal-content").html("");
                $("#modal-question").modal("show");
            },
            success: function (data) {

                $("#modal-question .modal-content").html(data.html_form);
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
                $("#modal-question2 .modal-content").html("");
                $("#modal-question2").modal("show");
            },
            success: function (data) {

                $("#modal-question2 .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);

        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          success: function (data) {
            if (data.form_is_valid) {
              Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Your Question has been posted',
                button :'Ok',
                timer : 2500,
              });
              $("#question-table").html(data.html_question_list);
              $("#modal-question").modal("hide");
            }

            else {
              $("#modal-question .modal-content").html(data.html_form);
            }
          }
        });
        return false;
      }

    var updateForm = function () {
      var form = $(this);

      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            Swal.fire({
              icon: 'success',
              title: 'Success',
              text: 'Your Question has been updated',
              button :'Ok',
              timer : 2500,
            });
            $("#question-detail").html(data.html_question_detail);
            $("#modal-question").modal("hide");
          }

          else {
            $("#modal-question .modal-content").html(data.html_form);
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
        success: function (data) {
          data.preventDefault;
          if (data.form_is_valid) {
            Swal.fire({
              icon: 'success',
              title: 'Success',
              text: 'Your Question has been deleted',
              button :'Ok',
              timer : 2500
            }).then(function(){
              window.location.href = page_url
            });
            $("#question-table").html(data.html_question_list);
            $("#modal-question2").modal("hide");
          }

          else {
            $("#modal-question2 .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };


    /* Binding */
    $(".js-create-question").click(loadForm);
    $("#modal-question").on("submit", ".js-question-create-form", saveForm);

    // Update post
    $(".js-update-question").click(loadForm);
    $("#modal-question").on("submit", ".js-question-update-form", updateForm);
    // Delete post
    $(".js-delete-question").click(loadForm2);
    $("#modal-question2").on("submit", ".js-question-delete-form", delForm);
});