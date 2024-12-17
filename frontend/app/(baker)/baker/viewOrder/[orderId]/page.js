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
      <h1>
        <div className="d-flex flex-row">
          <span>{order.customer.name}'s Order</span>
          <select className="nice-select ">
            <option value={'preparing'} selected>
              Preparing
            </option>
            <option value={'prepared'}>Prepared</option>
          </select>
        </div>
      </h1>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Product Name</th>
            <th scope="col">Qty</th>
          </tr>
          {order.items.map((item, i) => {
            <tr>
              <td>{item.productName}</td>
              <td>{item.quantity}</td>
            </tr>;
          })}
          {order?.customCake.map((cake, i) => {
            return (
              <tr key={'custom-' + i}>
                <tr>
                  <td>{cake.cakeshape}</td>
                  <td>{cake.cakesize}</td>
                  <td>{cake.caketype}</td>
                  <td>{cake.message}</td>
                </tr>
                {cake.layers.map((layer, i) => {
                  return (
                    <tr>
                      <td>{'layer ' + i + 1}</td>
                      <td>{layer.innerFillings}</td>
                      <td>{layer.innerToppings}</td>
                      <td>{layer.outerCoating}</td>
                      <td>{layer.outerToppings}</td>
                    </tr>
                  );
                })}
              </tr>
            );
          })}
        </thead>
      </table>
    </>
  );
}
