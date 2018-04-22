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

import firebase from 'firebase';
import axios from 'axios'

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

export default class extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        data: null
      };
    }

    componentDidMount() {

        let self = this;

        console.log('Test');
        let previous_items = [];
        let current_items = [];

        let starCountRef = database.ref('/');
        starCountRef.on('value', function(snapshot) {
            let root_map = snapshot.val();
            for (let i = 0; i < Object.keys(root_map).length; i++) {
              let can_id = Object.keys(root_map)[i];
              let current_fullness = root_map[can_id].current_fullness;
              console.log("previous_items:");
              console.log(previous_items);
              if (previous_items.length > 0) {
                console.log('Checking if twilio needed');
                if (current_fullness.can_id === 'can_1' && previous_items[1].is_full === false && current_fullness.is_full === true) {
                  axios.get('http://localhost:5000/twilio')
                    .then(response => console.log(response))
                }
              }

              current_fullness.can_id = can_id;
              current_items.push(current_fullness);
            }

            if (current_items === previous_items) {
              return;
            }

            previous_items = JSON.parse(JSON.stringify(current_items));
            current_items = [];

            console.log('current items', previous_items);
            self.setState({
              data: {
                items: previous_items
              }
            });
        });

        //console.log(self.state.data);
    }

    render() {
        console.debug('state', this.state);
        if (this.state.data === null) {
          console.warn('loading');
          return (
            <main className="container">
              <h1>Loading</h1>
            </main>
          );
        }

        let items = this.state.data.items;

        let fulls = items
          .filter(function (item) {
            return item.is_full;
          })
          .map(function(item) {
          return  <li key={item.can_id}>
                    {item.can_id} is full!
                  </li>
          // -------------------^^^^^^^^^^^---------^^^^^^^^^^^^^^
        });

        return (
            <main className="container">
              <h3>Full Trash Cans</h3>
              <ul>
                {fulls}
              </ul>
            </main>
        );
    }
}