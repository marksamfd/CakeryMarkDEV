const j = {
  customer: {
    name: 'Anas Ahmad',
    phone: '0123456789',
  },
  items: [
    {
      productID: 2,
      quantity: 4,
    },
    {
      productID: null,
      quantity: 1,
    },
  ],
  orderDate: '2024-11-23T02:06:47.172561',
  orderID: 1,
};
export default async function Page({ params }) {
  const cookieStore = await cookies();
  const token = await cookieStore.get('token');
  const slug = (await params).orderId;
  const order = await (
    await fetch(
      `${process.env.backend}/cakery/user/baker/Orders/${slug}/details`,
      {
        headers: {
          Authorization: `Bearer ${token.value}`,
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      },
    )
  ).json();
  return (
    <>
      <h1>{order.customer.name}'s Order</h1>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Due Date</th>
            <th scope="col">Order ID</th>
            <th scope="col">Phone</th>
          </tr>
        </thead>
      </table>
    </>
  );
}
