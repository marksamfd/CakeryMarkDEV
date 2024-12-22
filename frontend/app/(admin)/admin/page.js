import PieChart from '@/app/(customer)/components/PieChart';
import LineChart from '@/componenets/lineChart';
import { cookies } from 'next/headers';
import Link from 'next/link';
import React from 'react';

const data = [
  {
    id: 'japan',
    color: 'hsl(172, 70%, 50%)',
    data: [
      {
        x: 'plane',
        y: 109,
      },
      {
        x: 'helicopter',
        y: 11,
      },
      {
        x: 'boat',
        y: 69,
      },
      {
        x: 'train',
        y: 80,
      },
      {
        x: 'subway',
        y: 216,
      },
      {
        x: 'bus',
        y: 172,
      },
      {
        x: 'car',
        y: 239,
      },
      {
        x: 'moto',
        y: 18,
      },
      {
        x: 'bicycle',
        y: 266,
      },
      {
        x: 'horse',
        y: 298,
      },
      {
        x: 'skateboard',
        y: 219,
      },
      {
        x: 'others',
        y: 204,
      },
    ],
  },
];

const pie = [
  {
    id: 'css',
    label: 'css',
    value: 151,
    color: 'hsl(70, 70%, 50%)',
  },
  {
    id: 'java',
    label: 'java',
    value: 103,
    color: 'hsl(94, 70%, 50%)',
  },
  {
    id: 'haskell',
    label: 'haskell',
    value: 160,
    color: 'hsl(111, 70%, 50%)',
  },
  {
    id: 'rust',
    label: 'rust',
    value: 231,
    color: 'hsl(319, 70%, 50%)',
  },
  {
    id: 'php',
    label: 'php',
    value: 291,
    color: 'hsl(290, 70%, 50%)',
  },
];
async function Page() {
  const cookieStore = await cookies();
  const token = await cookieStore.get('token');
  const orders = await (
    await fetch(`${process.env.backend}/cakery/user/admin/Dashboard`, {
      headers: {
        Authorization: `Bearer ${token.value}`,
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
    })
  ).json();
  const lineChart = orders.data['total_price_by_date'];
  const dataLine = lineChart.map((e) => {
    return { x: e['Date'], y: e['Total Price'] };
  });
  const bestSold = orders.data['best_sold_items'];
  const bestSoldPie = bestSold.map((e) => {
    return { label: e['Date'], value: e['qty'] };
  });
  return (
    <div className="container h-100">
      <div className="row h-50 w-100">
        <div className="col-lg">
          <LineChart data={dataLine} />
        </div>
        <div className="w-100 d-lg-none d-sm-block"></div>
        <div className="col-lg">
          <PieChart data={bestSoldPie} />
        </div>
      </div>
      <div className="row h-50">
        <div className="col">
          <table className="table table-striped">
            <thead>
              <tr>
                <th scope="col">Product</th>
                <th scope="col">Number of Orders</th>
                <th scope="col">Price</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((el) => {
                <tr>
                  <th scope="row">{el.itemName}</th>
                  <td>{el['qty']}</td>
                  <td>{el['price']}</td>
                </tr>;
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Page;
