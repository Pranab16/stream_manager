var tweet_count_elem = document.getElementById('tweet_count');
var user_count_elem = document.getElementById('user_count');
var user_name_elem = document.getElementById('user_screen_name');

// this is called when connection is ready with swampdragon
swampdragon.ready(function() {
    // Subscribe users and tweets routers to watch their models
    swampdragon.subscribe('users', 'local-channel', null);
    swampdragon.subscribe('tweets', 'local-channel', null);
});

// this is called whenever a new object(of any model being watched) is created
swampdragon.onChannelMessage(function (channels, message) {

    if(message.data._type == 'tweet'){
        tweet_count_elem.innerHTML = Number(tweet_count_elem.innerHTML) + 1;

        // Fetch and update screen name having maximum tweets
        swampdragon.callRouter('get_screen_name', 'users', {}, function (context, data) {
            user_name_elem.innerHTML = data.screen_name;
        });

    }else if(message.data._type == 'user'){
        user_count_elem.innerHTML = Number(user_count_elem.innerHTML) + 1;
    }

});
