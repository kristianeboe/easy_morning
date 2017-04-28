import {
  Template
} from 'meteor/templating';
import {
  ReactiveVar
} from 'meteor/reactive-var';

import './main.html';


// Template.hello.onCreated(function helloOnCreated() {
//   // counter starts at 0
//   this.counter = new ReactiveVar(0);
// });

// Template.hello.helpers({
//   counter() {
//     return Template.instance().counter.get();
//   },
// });

// Template.hello.events({
//   'click button'(event, instance) {
//     // increment the counter when button is clicked
//     instance.counter.set(instance.counter.get() + 1);
//   },
// });

Template.add_alarm.events({
  'submit' (event, instance) {
    event.preventDefault();
    const form = event.target;
    const alarm_name = form.alarm_name.value
    const wake_up_time = form.wake_up_time.value
    const wake_up_threshold = form.wake_up_threshold.value

    const selected_days = document.querySelectorAll('#wake_up_days option:checked');
    const wake_up_days_values = Array.from(selected_days).filter(el => el.value != "").map((el) => {
      return el.value
        });
  
    alarm = {
      'name': alarm_name,
      'wake_up_time': wake_up_time,
      'wake_up_threshold': wake_up_threshold,
      'wake_up_days': wake_up_days_values,
      'on': true
    }

    Meteor.call('create_alarm', alarm)
    event.target.reset();
  }
})

Template.alarm_list.helpers({
  alarms() {
    user_id = Meteor.userId()
    alarms = AlarmDB.find({ userId: user_id }).fetch()
    console.log(alarms)

    return alarms
  },
  week() {
    return [
      {
        'day_num': '0',
        'day_name': 'Monday'
      },
      {
        'day_num': '1',
        'day_name': 'Tuesday'
      },
      {
        'day_num': '2',
        'day_name': 'Wednesday'
      },
      {
        'day_num': '3',
        'day_name': 'Thursday'
      },
      {
        'day_num': '4',
        'day_name': 'Friday'
      },
      {
        'day_num': '5',
        'day_name': 'Saturday'
      },
      {
        'day_num': '6',
        'day_name': 'Sunday'
      },
    ]
  },
  wake_up_day(alarm, day) {
    if(alarm.wake_up_days.indexOf(day.day_num) >= 0) {
      return 'selected'
    }
    return ''
  }
})

Template.alarm_list.events({
  'click .remove_alarm' (event, instance) {
    target = event.target
    _id = target.id.substr(7)
    Meteor.call('remove_alarm', _id)
  },
  'click .switch' (event) {
    _id = event.target.id.substr(3)
    Meteor.call('update_on_off', _id)
  }
})