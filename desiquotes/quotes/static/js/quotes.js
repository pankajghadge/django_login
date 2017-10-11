$(function () {
  $(".publish").click(function () {
    $("input[name='status']").val("P");
    $("form").submit();
  });

  $(".draft").click(function () {
    $("input[name='status']").val("D");
    $("form").submit();
  });

  $(".preview").click(function () {
    $.ajax({
      url: '/quotes/preview/',
      data: $("form").serialize(),
      cache: false,
      type: 'post',
      beforeSend: function () {
        $("#preview .modal-body").html("<div style='text-align: center; padding-top: 1em'><img src='/static/img/loading.gif'></div>");
      },
      success: function (data) {
        $("#preview .modal-body").html(data);
      }
    });
  });

  $(".remove-quote").click(function () {
    var quote_obj = $(this);
    var quote = $(this).attr("quote-id");
    var csrf = $(this).attr("csrf");
    $.ajax({
      url: '/quotes/remove/',
      data: {
        'quote': quote,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        alert($(quote_obj).attr("quote-id"));
        $(quote_obj).closest("div.item").fadeOut(400, function () {
	  alert($(quote_obj).closest("div.item").html());
          $(quote_obj).closest("div.item").remove();
        });
      }
    });
  });

});
