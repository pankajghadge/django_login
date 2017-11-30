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
    var quote    = $(this).closest("div.item");
    var quote_id = $(quote).attr("quote-id");
    var csrf     = $(quote).attr("csrf");
    var answer = confirm('Do you want to delete?');
    if(!answer) {
	return false;
    }
    $.ajax({
      url: '/quotes/remove/',
      data: {
        'quote': quote_id,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $(quote).fadeOut(400, function () {
          $(quote).remove();
        });
      }
    });
  });

  $(".like").click(function () {
    var quote    = $(this).closest("div.item");
    var quote_id = $(quote).attr("quote-id");
    var csrf     = $(quote).attr("csrf");
    $.ajax({
      url: '/quotes/like/',
      data: {
        'quote': quote_id,
        'csrfmiddlewaretoken': csrf
      },
      type: 'post',
      cache: false,
      success: function (data) {
        if ($(".like", quote).hasClass("unlike")) {
          $(".like", quote).removeClass("unlike");
          $(".like .text", quote).text("Like");
        }
        else {
          $(".like", quote).addClass("unlike");
          $(".like .text", quote).text("Unlike");
        }
        $(".like .like-count", quote).text(data);
      }
    });
  });
 

});
