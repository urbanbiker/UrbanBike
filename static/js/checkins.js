(function(){

     var Checkin = Backbone.Model.extend(
         {
             idAttribute: "_id",
             urlRoot: '/checkins/'
         });

    
     var Checkins = Backbone.Collection.extend({
             model: Checkin,
             url: function() {
                 if (_.isUndefined(this.options.center)) {
                     return '/checkins/';
                 } else {
                     return '/checkins/?lat=' + this.options.center[0] + '&lng=' + this.options.center[1];    
                 }
             },

             initialize: function(options) {
                 this.options = options;
             }                                                    
         }
     );

     // GoogleMap global objects
     window.infowindow = new google.maps.InfoWindow();

     var CheckinView = Backbone.View.extend(
         {
             template: $('#checkin-template'),
             events: {
                 "click a": "renderInfoWindow"
             },
         
             render: function() {
                 this.el = this.template.tmpl(this.model.toJSON());
                 this.delegateEvents();
                 return this;
             },
             
             renderInfoWindow: function() {
                 if (_.isUndefined(this.model)) {
                     window.infowindow.close();
                     return false;
                 } else {
                     var loc = this.model.get('location');
                     window.infowindow.setPosition(new google.maps.LatLng(loc[0], loc[1]));
                     var infowindow_view = new CheckinView({el: this.el.clone()});
                     window.infowindow.setContent(infowindow_view.el[0]);
                     window.infowindow.open(window.map);
                     return infowindow_view;
                 }
             }
                                                
         });

     var CheckinListView = Backbone.View.extend(
         {
             el: $("#checkin_list"),

             addCheckin: function(checkin_data) {
                 var self = this;
                 this.collection.create(
                     checkin_data, 
                     {
                         wait: true,
                         'success': function(model, responce) {
                             self.renderCheckin(model).renderInfoWindow();
                             $('#empty-message').hide();
                         }   
                     });
             },
             
             renderCheckin: function(checkin) {
                 var view = new CheckinView({model: checkin});
                 this.el.prepend(view.render().el);
                 return view;
             },
             
             render: function (){
                 var self = this;
                 this.collection.each(function(model, index){
                                      self.renderCheckin(model);
                                   });
                 return this;
             }
                                                
         });


     window.CheckinsApp = Backbone.View.extend(
         {
             el: $('body'),
             events: {
                 "click #do-checkin": "doCheckin"
             },

             initialize: function(options){
                 window.map = this.initialize_map();
                 this.geocoder = new google.maps.Geocoder();
                 this.checkinsView = new CheckinListView({collection: new Checkins(this.options.checkins)});
                 this.checkinsView.render();
             },

             doCheckin: function() {
                 var self = this;
                 navigator.geolocation.getCurrentPosition(function(position) {
                 var initialLocation = new google.maps.LatLng(position.coords.latitude, 
							      position.coords.longitude);
                     window.map.setCenter(initialLocation);
                     self.geocoder.geocode(
                         {
                             'latLng': initialLocation
                         }, 
                         function(results, status) {
                             if (status == google.maps.GeocoderStatus.OK) {
                                 self.checkinsView.addCheckin(
                                     {geocode: results, 
                                      location: {
                                          lat: position.coords.latitude, 
                                          lng: position.coords.longitude
                                      }});
                             } else {
                                 alert("Geocoder failed due to: " + status);
                             }
                         });
                                                              
                  });
                  return false;
             },

             initialize_map: function() {
                 var self = this;
	         var center = new google.maps.LatLng(
                     this.options.center[0], 
		     this.options.center[1]);
                 var myOptions = {
		     zoom: 15,
		     center: center,
		     mapTypeId: google.maps.MapTypeId.HYBRID,
		     mapTypeIds: [google.maps.MapTypeId.ROADMAP,
			          google.maps.MapTypeId.SATELLITE,
                                  google.maps.MapTypeId.HYBRID]
                 };
                 var map = new google.maps.Map(document.getElementById('map_canvas'),
					       myOptions);
                 map.setTilt(45);
                 map.setHeading(90);
                 self.addLegend(map);
                 var georssLayer = new google.maps.KmlLayer(self.options.geo_rss_url);
                 georssLayer.setMap(map);
                 var bikeLayer = new google.maps.BicyclingLayer();
                 bikeLayer.setMap(map);
                 return map;
             },

	     addLegend: function (map) {
                 var legendWrapper = document.createElement('div');
                 legendWrapper.id = 'legendWrapper';
                 legendWrapper.index = 1;
                 if ($("#checkin-button").length) {
                     legendWrapper.appendChild($("#checkin-button").clone().show()[0]);
                     map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legendWrapper);
                 }
	     }
         });
})();