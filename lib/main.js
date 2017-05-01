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

        Meteor.call('update_ras_pi')

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
});