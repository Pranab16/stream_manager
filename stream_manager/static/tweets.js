var hashtag = '';
$('#tweet_results').hide();

// this is called when connection is ready with swampdragon
swampdragon.ready(function() {
    // Subscribe users and tweets routers to watch their models
    swampdragon.subscribe('users', 'local-channel', null);
    swampdragon.subscribe('tweets', 'local-channel', null);
});

// this is called whenever a new object(of any model being watched) is created
swampdragon.onChannelMessage(function (channels, message) {
    if(message.data._type == 'tweet' && message.data.hashtag == hashtag){

        // fetch and set tweets count
        swampdragon.callRouter('get_count', 'tweets', {hashtag: hashtag}, function (context, data) {
            $('#tweet_count').text(data.tweet_count);
        });

        // Fetch and update screen name having maximum tweets
        swampdragon.callRouter('get_screen_name', 'users', {hashtag: hashtag}, function (context, data) {
            $('#user_screen_name').text(data.screen_name);
        });
        $('#tweet_results').show(); //show new tweet results

    }else if(message.data._type == 'user'){
        // fetch and set users count
        swampdragon.callRouter('get_count', 'users', {hashtag: hashtag}, function (context, data) {
            $('#user_count').text(data.user_count);
        });
    }


});

var start_track = function(url, csrf_token){
    $('#track_hashtag').click(function(){
        hashtag = $('#hashtag').val();
        if(hashtag !== ''){
            // ajax call to start tracking new hashtag
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    csrfmiddlewaretoken: csrf_token,
                    hashtag: hashtag
                }
            });
        }

        $('#tweet_results').hide(); // hide the old tweet results

    });
};
