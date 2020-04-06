$('.permission-area .parent').click(function(){
  
  $(this).find('.drop-down').toggleClass('fa-caret-right');
  $(this).nextUntil('.parent').toggle('hide')
});