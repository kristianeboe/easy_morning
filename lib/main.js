import {
    HTTP
} from 'meteor/http'

AlarmDB = new Mongo.Collection('alarmDB');

Meteor.methods({
    'create_alarm' (alarm) {

        user = Meteor.userId()

        alarm_object = Object.assign(alarm, {
            'userId': user
        })
        console.log("hello")
        console.log(alarm_object)

        AlarmDB.insert(alarm_object)

        $(document).ready(function () {
            $('select').material_select();
        });

    },
    'remove_alarm' (_id) {
        AlarmDB.remove(_id);
    },
    'update_on_off' (_id) {
        alarm = AlarmDB.findOne(_id);
        AlarmDB.update(_id, {
            $set: {
                on: !alarm.on
            }
        });
    },
    'update_ras_pi' () {
        alarms = AlarmDB.find().fetch();
        console.log(alarms)

        HTTP.call(
            'POST',
            'http://129.241.209.166:9966', 
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
});