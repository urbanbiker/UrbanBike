(function(){
     var Tweet = Backbone.Model.extend(
         {
             urlRoot: '/twitter/tweets/'
         });
    

     var Tweets = Backbone.Collection.extend(
         {
             model: Tweet,
             url: function() {
                 return '/twitter/tweets/?lat=' + this.options.center[0] + '&lng=' + this.options.center[1];
             },

             initialize: function(options) {
                 this.options = options;
             }
             
         });


     var TwitterView = Backbone.View.extend(
         {
             template: $('#twitter-template'),
             events: {
                 "click a": "renderInfoWindow"
             },

             render: function() {
                 this.el = this.template.tmpl(this.model.toJSON());
                 this.delegateEvents();
                 return this;
             },

             renderInfoWindow: function() {
                 // we are rendering info window with the same template here
                 if (_.isUndefined(this.model)) {
                     infowindow.close();
                     return false;
                 } else {
                     var loc = this.model.get('geo').coordinates;
                     infowindow.setPosition(new google.maps.LatLng(loc[0], loc[1]));
                     var infowindow_view = new TwitterView({el: this.el.clone()});
                     infowindow.setContent(infowindow_view.el[0]);
                     infowindow.open(map);
                     return infowindow_view;
                 }
             }
                                                             
         });


      window.TwitterApp = Backbone.View.extend(
         {
             el: $("#twitter-feed"),
             
             initialize: function(options){
                 var self = this;
                 this.tweets = new Tweets({center: this.options.center});
                 this.tweets.fetch(
                     {
                         success: function(collection, responce) {
                             self.el.find('#loading-spin').hide();
                             collection.each(function(model, index) {
                                                 self.renderTweet(model);
                                             });
                             twttr.anywhere(function (T) {
	                                        T("#tweets h4 a").hovercards(
                                                    { 
                                                        linkify: false,
                                                        username: function(node) {
                                                            return node.title;
                                                        }
                                                    });
	                                    }); 
                         }
                     });
             },
             
             renderTweet: function(media) {
                 var view = new TwitterView({model: media});
                 this.el.append(view.render().el);
                 return view;
             },
             
             render: function (){
                 var self = this;
                 this.photos.each(function(model, index){
                                      self.renderTweet(model);
                                   });
                 return this;
             }
                                                
         });

})();