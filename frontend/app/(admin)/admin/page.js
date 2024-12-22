import PieChart from '@/app/(customer)/components/PieChart';
import LineChart from '@/componenets/lineChart';
import Link from 'next/link';
import React from 'react';

const data = [
  {
    id: 'Cakes',
    color: 'hsl(172, 70%, 50%)',
    data: [
      {
        x: 'Tarts',
        y: 109,
      },
      {
        x: 'Sugar',
        y: 11,
      },
      {
        x: 'Cupcakes',
        y: 69,
      },
      {
        x: 'Pastries',
        y: 80,
      },
      {
        x: 'sugar',
        y: 216,
      },
      {
        x: 'others',
        y: 172,
      },
      {
        x: 'red-velvet',
        y: 239,
      },
      {
        x: 'chocolate',
        y: 18,
      },
      {
        x: 'vanilla',
        y: 266,
      },
      {
        x: 'strawberry',
        y: 298,
      },
      {
        x: 'mango',
        y: 219,
      },
      {
        x: 'blueberry',
        y: 204,
      },
    ],
  },
];

const pie = [
  {
    id: 'cakes',
    label: 'Cakes',
    value: 151,
    color: 'hsl(70, 70%, 50%)',
  },
  {
    id: 'tarts',
    label: 'Tarts',
    value: 103,
    color: 'hsl(94, 70%, 50%)',
  },
  {
    id: 'cupcakes',
    label: 'Cupcakes',
    value: 160,
    color: 'hsl(111, 70%, 50%)',
  },
  {
    id: 'pastries',
    label: 'Pastries',
    value: 231,
    color: 'hsl(319, 70%, 50%)',
  },
  {
    id: 'sugar',
    label: 'Sugar',
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
              {/* {orders.map((el) => { */}
              <tr>
                {/* <th scope="row">1</th> */}
                <td>{'Cupcake'}</td>
                <td>500</td>
                <td>15$</td>
              </tr>
              <tr>
                {/* <th scope="row">1</th> */}
                <td>{'Tart'}</td>
                <td>500</td>
                <td>15$</td>
              </tr>
              {/* })} */}
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
