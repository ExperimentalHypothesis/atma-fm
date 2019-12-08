
var imgSRC={'src1':'app\static\img\play.png','src2': 'app\static\img\pause.png' }

$('.image1').toggle(function(){
      $(this).attr('src',imgSRC.src2)
   }, function() {
       $(this).attr('src',imgSRC.src1)
   }
});