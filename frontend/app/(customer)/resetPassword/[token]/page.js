import Button from '../../components/button';
import CheckoutInputField from '../../components/checkoutInput';
import Title from '../../components/title';

async function resetPassword({ params }) {
  /*  async function resetPassswordForm(fd) {
    'use server';
    const order = await (
      await fetch(`${process.env.backend}/user/baker/orders`, {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
      })
    ).json();
  } */
  return (
    <div className="container">
      <Title>Reset your Password</Title>
      <from action={resetPassswordForm} className="d-flex flex-column">
        <CheckoutInputField name={'password'} label={'Password'} />
        <CheckoutInputField
          name={'confirmPassword'}
          label={'Confirm Password'}
        />
        <Button type={'submit'} classNameProp={'w-100'}>
          Submit
        </Button>
      </from>
    </div>
  );
}

export default resetPassword;
