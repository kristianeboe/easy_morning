import {
  Meteor
} from 'meteor/meteor';

Meteor.startup(() => {
  // code to run on server at startup
});


Meteor.methods({
  'update_ras_pi' () {
    alarms = AlarmDB.find().fetch();

    HTTP.post(
      "http://localhost:9966",
      // "http://127.0.0.1:4040",
      // "http://e615520c.ngrok.io",
      {
        data: alarms
      },
      function (error, response) {
        if (error) {
          console.log(error);
        } else {
          console.log(response);
        }
      })
  },
})