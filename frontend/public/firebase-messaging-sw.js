// eslint-disable-next-line no-undef
importScripts('https://www.gstatic.com/firebasejs/8.8.0/firebase-app.js');
// eslint-disable-next-line no-undef
importScripts('https://www.gstatic.com/firebasejs/8.8.0/firebase-messaging.js');

const firebaseConfig = {
  apiKey: 'AIzaSyBq1Y0gIa0QiEY84oUZ1RJBcu8tgzWAOIs',
  authDomain: 'cakery-b599e.firebaseapp.com',
  projectId: 'cakery-b599e',
  storageBucket: 'cakery-b599e.firebasestorage.app',
  messagingSenderId: '318553962335',
  appId: '1:318553962335:web:6e13759233f512f862a8ea',
};
// eslint-disable-next-line no-undef
firebase.initializeApp(firebaseConfig);
// eslint-disable-next-line no-undef
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
  console.log(
    '[firebase-messaging-sw.js] Received background message ',
    payload,
  );
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: './favicon.ico',
  };
  console.log(self.registration);
  self.registration.showNotification(notificationTitle, notificationOptions);
});
