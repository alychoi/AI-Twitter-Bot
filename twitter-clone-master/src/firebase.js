import firebase from "firebase";

const firebaseConfig = {
  apiKey: "AIzaSyAY34HYZZOjK6cELn5bsFmhuVg4JIQU99w",
  authDomain: "twitter-clone-80959.firebaseapp.com",
  databaseURL: "https://twitter-clone-80959-default-rtdb.firebaseio.com",
  projectId: "twitter-clone-80959",
  storageBucket: "twitter-clone-80959.appspot.com",
  messagingSenderId: "46692477147",
  appId: "1:46692477147:web:589ea7712d2d7be9e204fe",
  measurementId: "G-DRGVVTGB9G"
};

const firebaseApp = firebase.initializeApp(firebaseConfig);

const db = firebaseApp.firestore();

export default db;
