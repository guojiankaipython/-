    $('.item .title').click(function () {
      $(this).next().toggle().toggleClass('hidden').parent().siblings().children('.body').addClass('hidden');
    });