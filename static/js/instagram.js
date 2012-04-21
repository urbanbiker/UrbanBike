(function(){

     var Photo = Backbone.Model.extend(
         {
             urlRoot: '/instagram/photos/'
         });
    

     var Photos = Backbone.Collection.extend({
             model: Photo,
             url: function() {
                 return '/instagram/photos/?lat=' + this.options.center[0] + '&lng=' + this.options.center[1];
             },

             initialize: function(options) {
                 this.options = options;
             }

         }
     );


     var InstagrInfoWindow = Backbone.View.extend(
         {
             template: $('#instagram-info-template'),
             events: {
                 "click a": "closeInfoWindow"
             },
             
             render: function() {
                 this.el = this.template.tmpl(this.model.toJSON());
                 this.delegateEvents();
                 var point = this.model.get('location').point;
                 window.infowindow.setPosition(new google.maps.LatLng(
                                                   point.latitude, 
                                                   point.longitude));
                 window.infowindow.setContent(this.el[0]);
                 window.infowindow.open(window.map);
                 return this;
             },

             closeInfoWindow: function() {
                 window.infowindow.close();
                 return false;
             }
         });


     var MediaView = Backbone.View.extend(
         {
             tagName:  "figure",
             template: $('#instagram-template'),
             events: {
                 "click a": "renderInfoWindow"
             },

             render: function() {
                 this.el = this.template.tmpl(this.model.toJSON());
                 this.delegateEvents();
                 return this;
             },

             renderInfoWindow: function() {
                 var infowindow_view = new InstagrInfoWindow({model: this.model});
                 infowindow_view.render();
                 return infowindow_view;
             }
                                                             
         });


      window.InstagramApp = Backbone.View.extend(
         {
             el: $("#instagram-photos"),
             
             initialize: function(options){
                 var self = this;
                 this.photos = new Photos({center: this.options.center});
                 this.photos.fetch(
                     {
                         success: function(collection, responce) {
                             self.el.find('#loading-spin').hide();
                             var big_images = [];
                             collection.each(function(model, index){
                                                 self.renderMedia(model);
                                                 big_images.push(model.get('images').standard_resolution.url);
                                             });
                             $('#kenburns:visible').kenburns({images:big_images});
                         } 
                     });
             },
             
             renderMedia: function(media) {
                 var view = new MediaView({model: media});
                 this.el.append(view.render().el);
                 return view;
             },
             
             render: function (){
                 var self = this;
                 this.photos.each(function(model, index){
                                      self.renderMedia(model);
                                  });
                 return this;
             }
                                                
         });

})();