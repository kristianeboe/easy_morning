import { Meteor } from 'meteor/meteor';

Meteor.startup(() => {
  // code to run on server at startup
});


Meteor.methods({
  'update_ras_pi' () {
        alarms = AlarmDB.find().fetch();
        console.log(alarms)

        HTTP.call(
            'POST',
            // 'https://129.241.209.166:9966', 
            'https://pi@0.tcp.ngrok.io:9966', 
            {
                data: {
                    alarm_list: alarms
                },
            },
            function( error, response ) {
                if ( error ) {
                    console.log("error")
                    console.log( error );
                } else {
                    console.log("response")
                    console.log( response );
                }
            })
    }
})