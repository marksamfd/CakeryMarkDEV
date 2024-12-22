import React from 'react';
import Breadcrumb from '@/app/(customer)/components/breadcrumb';
import { cookies } from 'next/headers';

/**
 * NotificationsPage component.
 *
 * This component is used to display the notifications history of the customer.
 *
 * @returns {ReactElement} The NotificationsPage component.
 */
async function NotificationsPage() {
  const cookieStore = cookies();
  const token = cookieStore.get('token')?.value;

  let notifications = [];
  try {
    if (token) {
      const response = await fetch(`${process.env.backend}/cakery/user/customer/Notifications`, {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: 'application/json',
          'Content-Type': 'application/json',
        }
      });

      notifications = await response.json();
    }
  }
  catch (err) {
    console.log("error fetching notification", err);
  }

  return (
    <div>
      <div style={{ marginBottom: '50px' }}>
        <Breadcrumb title="Notifications History" />
      </div>
      <div className="container mt-5">
        <div style={{ overflowY: 'auto', display: 'block', height: '500px' }}>
          <table style={{ width: '100%' }}>
             <tbody>
              {notifications.map((notification, i) => (
                <tr key={notification.id} className="notification-row">
                 <td style={{ minWidth: '50px' }}>{i + 1}</td>
                 <td style={{ minWidth: '250px' }}>
                    {notification.message}
                     {notification.id && <span style={{marginLeft:'5px'}}> (Order ID: {notification.id})</span>}
                   </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
       <br />
    </div>
  );
}

export default NotificationsPage;