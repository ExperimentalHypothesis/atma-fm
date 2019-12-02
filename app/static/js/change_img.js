<script>
function toggleImage() {
   var img1 = "http://placehold.it/350x150";
   var img2 = "http://placehold.it/200x200";
   var imgElement = document.getElementById('toggleImage');
   imgElement.src = (imgElement.src === img1)? img2 : img1;
}
</script>