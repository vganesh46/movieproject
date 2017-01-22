var mongoose = require('mongoose'),
    fs = require('fs'),
    twitter = require('ntwitter'),
    Tweet = require('./models/Tweet');
 
var keys = {
    consumer_key : "GrUmb0gEqnyF3GIFXSr0l9mXX",
    consumer_secret : "6GSKBGdNm7V18GjWmOEX8VHA0N7AMYkVRonWvU9BryYqmVTmAF",
    token : "4714359180-4TNaNM2fuJLtrtsMrUaZDvuMQb4VsEk1QSBsGK5",
    token_secret : "BRFk5QEgOKTl1O7yfRtdZkKjJMhLL1RVRuCRKqgd4clEt"
};

mongoose.connect('mongodb://localhost/tweets-InfernoIlFilm-movie');

//var Twitter = new TwitterStream(keys, false);
//Twitter.stream('statuses/filter', {
//    track: '#Majnu'
//});
//
//Twitter.on('connection success', function (uri) {
//    console.log('connection success', uri);
//});
//
//Twitter.on('connection rate limit', function (httpStatusCode) {
//    console.log('connection rate limit', httpStatusCode);
//});
//
//Twitter.on('data', function (data) {
//    var tweet = data.toString('utf8');
//    console.log('data', tweet["id"]);
//    console.log('Text : ', tweet["text"]);
//    // console.log('Screen Name : ', tweet['user']['screen_name']);
//});
// 
//Twitter.pipe(fs.createWriteStream('tweets.json'));

// var twitter = require('ntwitter');

var twit = new twitter({
    consumer_key : "GrUmb0gEqnyF3GIFXSr0l9mXX",
    consumer_secret : "6GSKBGdNm7V18GjWmOEX8VHA0N7AMYkVRonWvU9BryYqmVTmAF",
    access_token_key : "4714359180-4TNaNM2fuJLtrtsMrUaZDvuMQb4VsEk1QSBsGK5",
    access_token_secret : "BRFk5QEgOKTl1O7yfRtdZkKjJMhLL1RVRuCRKqgd4clEt"
});

twit.stream('statuses/filter', {track:'#InfernoIlFilm'}, function(stream) {
  stream.on('data', function (data) {
    var tweet = {
      twid: data['id'],
      active: false,
      author: data['user']['name'],
      avatar: data['user']['profile_image_url'],
      body: data['text'],
      date: data['created_at'],
      screenname: data['user']['screen_name'],
      hashtag : 'InfernoIlFilm'
    };
    var tweetEntry = new Tweet(tweet);
    // Save 'er to the database
    tweetEntry.save(function(err) {
      if (!err) {
        // console.log(tweet);
      }
    });
  });
  stream.on('end', function (response) {
    // Handle a disconnection
      console.log('End : ' + response);
  });
  stream.on('destroy', function (response) {
    // Handle a 'silent' disconnection from Twitter, no end/error event fired
      console.log('destroy : ' + response);
  });
    stream.on('error', function(error, code) {
console.log("My error: " + error + ": " + code);
});
  // Disconnect stream after five seconds
 // setTimeout(stream.destroy, 5000);
});