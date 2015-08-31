$(function () {

  $('.alert .close').click(function () {
    $(this).closest('.alert').fadeOut(300, function () {
      $(this).remove();
    });
  });

  var updateTime = function () {
    var time = moment().tz('UTC').format('dddd, MMMM D YYYY, HH:mm:ss ZZ [UTC]');
    $('.utc').html(time);
    setTimeout(updateTime, 500);
  };

  updateTime();

});
