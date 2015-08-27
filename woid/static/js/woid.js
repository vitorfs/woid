$(function () {

  $('.alert .close').click(function () {
    $(this).closest('.alert').fadeOut(300, function () {
      $(this).remove();
    });
  });

});
