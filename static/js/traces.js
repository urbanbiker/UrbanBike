(function(){

     var Trace = Backbone.Model.extend(
         {
             urlRoot: '/traces/'
         });

     var Point = Backbone.Model.extend(
         {
         });

    
     var Traces = Backbone.Collection.extend({
             model: Trace,
             url: function() {
                 return '/traces/';
             },

             initialize: function(options) {
                 this.options = options;
             }                                                    
         }
     );

     var Points = Backbone.Collection.extend({
             model: Point,
             localStorage: new Backbone.LocalStorage("SomeCollection"),
             initialize: function(options) {
                 this.options = options;
             }                                                    
         }
     );
     
     var TraceView = Backbone.View.extend(
         {
             events: {
                 "click #start-record": "start_record",
                 "click #stop-record": "stop_record"
             },

             initialize: function() {
                 this.cache = new Points();
                 //this.geocoder = new google.maps.Geocoder();
             },                                               
         
             
             render_collection: function(collection) {
                 var self = this;
                 var coords = [];
                 collection.each(function(model, index){
                                     coords.push(new google.maps.LatLng(
                                                     model.get('lat'), 
                                                     model.get('lng')));
                                 });
                 var the_path = new google.maps.Polyline(
                     {
                         path: coords
                     });
                 the_path.setMap(this.options.map);
                 if (coords.length){
                     this.options.map.setCenter(coords[0]);    
                 }
                 
                 
                 return this.el;
             },

             render_marker: function(coords) {                 
                 var beachMarker = new google.maps.Marker(
                     {
                         position: coords,
                         map: this.options.map
                     });
             },
                          
             start_record: function() {
                 var self = this;
                 this.watchId = navigator.geolocation.watchPosition(
                     function(position) {
                         var the_point = self.cache.create(
                             {lat: position.coords.latitude,
                              lng: position.coords.longitude,
                              speed: position.coords.longitude,
                              timestamp: position.timestamp}); 
                         var lat_lng = new google.maps.LatLng(position.coords.latitude,
                                                              position.coords.longitude);
                         self.render_marker(lat_lng);
                     });
                 return false;
             },
                          
             stop_record: function() {
                 navigator.geolocation.clearWatch(this.watchId);
                 this.render_collection(this.cache);
                 this.model.save({points: this.cache.toJSON()});
                 this.collection.add(this.cache);
                 this.cache.reset([]);
                 return false;
             }
         });

     window.TraceApp = Backbone.View.extend(
         {
             initialize: function(){
                 var trace = new Trace({id: this.options.uuid});
                 var points = new Points(this.options.points);
                 
                 var view = new TraceView({model: trace,
                                           collection: points,
                                           map:  this.init_map(), 
                                           el: '#trace'});
                 view.render_collection(points);
                 if (this.options.fire_start){
                     view.start_record();
                 }
                     
             },

             init_map: function(){
                 var center = new google.maps.LatLng(
                     this.options.center[0], 
		     this.options.center[1]);
                 var myOptions = {
		     zoom: 15,
		     center: center,
		     mapTypeId: google.maps.MapTypeId.HYBRID,
		     mapTypeIds: [google.maps.MapTypeId.HYBRID]
                 };
                 var map = new google.maps.Map(document.getElementById('map_canvas'),
					       myOptions);
                 var bikeLayer = new google.maps.BicyclingLayer();
                 bikeLayer.setMap(map);
                 return map;
             }
         });
     
})();