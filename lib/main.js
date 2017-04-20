AlarmDB = new Mongo.Collection('alarmDB');

Meteor.methods({
    create_alarm (alarm) {
        //Objects.insert({_id: id, name:'test'});
        if(this.isSimulation) {
            appRouter.navigate("object/id/" + id, {trigger:true});
        }
    }
});