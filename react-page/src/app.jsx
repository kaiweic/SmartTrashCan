//import the React class from the `react` module
//this module is already listed as a dependency
//in our package.json file, so after running
//`npm install`, the "react" module will be in
//our node_modules directory, so we can import it
//simply by using the module name
import React from "react";

//polyfill for the fetch() API so that we can use
//it in Safari and older browsers
//this module was already included in our package.json
//so after you execute `npm install` this module will
//be in the node_modules directory, so we can load it
//simply by importing it's module name
import "whatwg-fetch";

import firebase from 'firebase'

//import our CSS file
//Webpack will actually merge the contents
//of this file into an inline <style></style>
//attribute within the <head> section, so that
//the browser doesn't have to make another
//network request to get the styles!
//note that here we start the path with a `.`
//to signal that this is a relative file
//path and not a module in our node_modules
//directory 
//import "./css/main.css";

export default class extends React.Component {
    constructor(props) {
        super(props);

        const self = this;

        // Initialize Firebase
        let config = {
            apiKey: "AIzaSyDLxi0Uiyzdt6Qkjh4wX3uVxWKYn4YdsBQ",
            authDomain: "smarttrashcan-a731b.firebaseapp.com",
            databaseURL: "https://smarttrashcan-a731b.firebaseio.com",
            projectId: "smarttrashcan-a731b",
            storageBucket: "smarttrashcan-a731b.appspot.com",
            messagingSenderId: "644066905865"
        };
        firebase.initializeApp(config);

        // Get a reference to the database service
        let database = firebase.database();

        let previous_items = [];
        let current_items = [];

        let starCountRef = database.ref('/');
        starCountRef.on('value', function(snapshot) {
            let root_map = snapshot.val();
            for (let i = 0; i < Object.keys(root_map).length; i++) {
              let can_id = Object.keys(root_map)[i];
              let current_fullness = root_map[can_id].current_fullness;
              current_fullness.can_id = can_id;
              current_items.push(current_fullness);
            }

            if (current_items === previous_items) {
              return;
            }
            previous_items = current_items;
            current_items = [];

            self.state = {
              data: {
                items: previous_items
              }
            };

            console.log(self.state);
        });
    }

    render() {
        return (
            <main className="container">
                <h1>Hello React!</h1>
                <div className="container" id="map-container">
                </div>
            </main>
        );
    }
}