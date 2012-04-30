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
             localStorage: new Backbone.LocalStorage("PointCollection"),
             initialize: function(options) {
                 this.options = options;
             }                                                    
         }
     );
     
     var TraceView = Backbone.View.extend(
         {
             events: {
                 "click a": "toggle_record"
             },

             toggle_record: function(){
                 if (this.status == 'off'){
                     this.status = 'on';
                     this.start_record();
                     this.el.find('span').text("pause || stop");
                     this.el.find('a').css({'background': '#E84C38'});
                     this.el.find('a').hover(
                         function(){
                             $(this).css('background', '#FFC300');
                         },
                         function(){
                             $(this).css('background', '#E84C38');
                         });

                 } else {
                     this.status = 'off';
                     this.stop_record();
                     this.el.find('span').text("resume");
                     this.el.find('a').css({background: '#FFC300'});
                     this.el.find('a').hover(
                         function(){
                             $(this).css('background', '#E84C38');
                         },
                         function(){
                             $(this).css('background', '#FFC300');
                         });

                 }
                 
                 return false;
             },

             initialize: function() {
                 var self = this;
                 this.el = $(this.el);
                 this.status = 'off';
                 //this.collection.bind('add', this.track_change);
                 this.map = window.gmaps.map;
                 this.geocoder = new google.maps.Geocoder();
                 this.polyline = new google.maps.Polyline({map: this.map, path: []});
                 this.infowindow = new google.maps.InfoWindow();
                 
                 $(window).bind('beforeunload', function() {
                                    if (this.status == 'on'){
                                        self.toggle_record();
                                    }
                                }); 
             },                                               
             
             track_change: function() {
             },

             renderInfoWindow: function(model) {
                 var self = this;
                 var location = new google.maps.LatLng(
                     model.get('lat'),  model.get('lng'));
                 
                 var marker = new google.maps.Marker(
                     {
                         map: this.map,
                         position: location
                     });
                 this.geocoder.geocode({
                         'latLng': location
                     }, 
                     function(results, status) {
                         if (status == google.maps.GeocoderStatus.OK) {
                             var content = results[0].formatted_address;
                             model.set({formatted_address: results[0].formatted_address});
                             content += "<br/>" + moment(model.get['timestamp']).format("MMM Do, h:mm:ss a");
                             self.infowindow.setPosition(location);
                             self.infowindow.setContent(content);
                             self.infowindow.open(self.map);
                         } 
                     });
                 this.map.setCenter(location);
                 this.map.setZoom(14);
                 
             },

             render: function() {
                 var self = this;
                 var the_path = this.polyline.getPath();
                 this.collection.each(function(model, index) {
                     the_path.push(new google.maps.LatLng(model.get('lat'),  model.get('lng')));
                 });
                 this.polyline.setPath(the_path);

                 if (this.collection.length > 0) {
                     this.renderInfoWindow(this.collection.at(
                                           this.collection.length -1));
                 }
                 return this.el;
             },
                          
             start_record: function() {
                 var self = this;
                 var model_dict = {};
                 this.updater = $.periodic(
                     function() {
                         navigator.geolocation.getCurrentPosition(
                             function(position) {
                                 if (position.coords.latitude != model_dict.lat && position.coords.longitude != model_dict.lng) {
                                     model_dict = {lat: position.coords.latitude,
                                                   lng: position.coords.longitude,
                                                   speed: position.coords.longitude,
                                                   timestamp: position.timestamp};
                                     var model = self.collection.create(model_dict); 
                                     if (self.collection.length == 1) {
                                         self.renderInfoWindow(model);
                                     }
                                 }
                             }, 
                             function() {
                                 //error handler here.
                             },
                             {
                                 enableHighAccuracy: true
                             }
                         );
                     });
             },
             stop_record: function() {
                 this.updater.cancel();
                 this.render();
                 this.model.save({points: this.collection.toJSON()});
                 this.collection.reset([]);
             }
         });

     window.TraceApp = Backbone.View.extend(
         {
             initialize: function(){
                 var trace = new Trace({id: this.options.uuid});
                 var points = new Points(this.options.points);
                 var view = new TraceView({model: trace,
                                           collection: points,
                                           el: '#nav'});
                 view.render();
                 if (this.options.fire_start){
                     view.toggle_record();
                 }
                     
             }

         });
     
})();