(function(){
     window.GMapsApp = Backbone.View.extend(
         {
             initialize: function(){
                 this.map = this.init_map(this.options.center);
             },

             init_map: function(center){
                 var map_options = {
		     zoom: 15,
                     center: new google.maps.LatLng(center[0], center[1]),
		     mapTypeId: google.maps.MapTypeId.HYBRID,
		     mapTypeIds: [google.maps.MapTypeId.HYBRID]
                 };
                 var map = new google.maps.Map(document.getElementById('map_canvas'), map_options);
                 var bikeLayer = new google.maps.BicyclingLayer();
                 bikeLayer.setMap(map);
                 return map;
             }
         });
     
})();