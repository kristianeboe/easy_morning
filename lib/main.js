AlarmDB = new Mongo.Collection('alarmDB');

Meteor.methods({
    'create_alarm' (alarm) {

        console.log(alarm)
        console.log(alarm.wake_up_days)
        const wake_up_days = alarm.wake_up_days.map((el) => {
            if (el.value == "0") {
                return "Monday";
            }
            if (el.value == "1") {
                return "Tuesday";
            }
            if (el.value == "2") {
                return "Wednesday";
            }
            if (el.value == "3") {
                return "Thursday";
            }
            if (el.value == "4") {
                return "Friday";
            }
            if (el.value == "5") {
                return "Saturday";
            }
            if (el.value == "6") {
                return "Sunday";
            }
        });


        AlarmDB.insert({
            'name': alarm.alarm_name,
            'wake_up_time': alarm.wake_up_time,
            'wake_up_days': wake_up_days,
            'on': true
        })
        // console.log(alarm_name)
        // console.log(wake_up_time)
        // console.log(wake_up_days)
        // console.log("Hello");

    },
})