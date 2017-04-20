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
    wake_up_time = form.wake_up_time.value

    const selected_days = document.querySelectorAll('#wake_up_days option:checked');
    const wake_up_days_values = Array.from(selected_days).filter(el => el.value != "")

    alarm = {
      'name': alarm_name,
      'wake_up_time': wake_up_time,
      'wake_up_days': wake_up_days_values,
      'on': true
    }

    Meteor.call('create_alarm', alarm)
    
  }
})

Template.alarm_list.helpers({
  alarms() {
    alarms_from_db = AlarmDB.find().fetch();
    // const alarms = alarms_from_db.map

    console.log(alarms_from_db)

    return alarms_from_db

    return [{
        'name': 'School',
        'wake_up_time': '0700',
        'wake_up_days': {
          'Monday': '',
          'Tuesday': '',
          'Wednesday': 'selected',
          'Thursday': 'selected',
          'Friday': '',
          'Saturday': '',
          'Sunday': ''
        },
        'on': true,
      },
      {
        'name': 'Work',
        'wake_up_time': '0700',
        'wake_up_days': {
          'Monday': 'selected',
          'Tuesday': '',
          'Wednesday': '',
          'Thursday': '',
          'Friday': 'selected',
          'Saturday': '',
          'Sunday': ''
        },
        'on': true,
      },
      {
        'name': 'Party',
        'wake_up_time': '1900',
        'wake_up_days': {
          'Monday': '',
          'Tuesday': '',
          'Wednesday': '',
          'Thursday': '',
          'Friday': 'selected',
          'Saturday': 'selected',
          'Sunday': ''
        },
        'on': false,
      },
    ]
  },
  week() {
    return [
      "Monday",
      "Tuesday",
      "Wednesday",
      "Thursday",
      "Friday",
      "Saturday",
      "Sunday",
    ]
  },
  wake_up_day(alarm_name, day) {
    if (alarm_name == "School" && (day == "Wednesday" ||  day == "Thursday")) {
      return 'selected'
    }
    if (alarm_name == "Work" && (day == "Monday" ||  day == "Friday")) {
      return 'selected'
    }

    return ''
  }
})
