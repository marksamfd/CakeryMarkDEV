import { initializeApp } from 'firebase/app';

const firebaseConfig = {
  apiKey: 'AIzaSyBq1Y0gIa0QiEY84oUZ1RJBcu8tgzWAOIs',
  authDomain: 'cakery-b599e.firebaseapp.com',
  projectId: 'cakery-b599e',
  storageBucket: 'cakery-b599e.firebasestorage.app',
  messagingSenderId: '318553962335',
  appId: '1:318553962335:web:6e13759233f512f862a8ea',
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);
export default firebaseApp;
