AlarmDB = new Mongo.Collection('alarmDB');

Meteor.methods({
    'create_alarm' (alarm) {

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

        console.log(alarm.name)

        AlarmDB.insert({
            'name': alarm.name,
            'wake_up_time': alarm.wake_up_time,
            'wake_up_days': wake_up_days,
            'on': true
        })
        // console.log(alarm_name)
        // console.log(wake_up_time)
        // console.log(wake_up_days)
        // console.log("Hello");

    },
    'remove_alarm' (_id) {
        AlarmDB.remove(_id);
    },
    'update_on_off' (_id) {
        alarm = AlarmDB.findOne(_id);
        AlarmDB.update(_id, {
            $set: { on: !alarm.on}
        });
    }
})