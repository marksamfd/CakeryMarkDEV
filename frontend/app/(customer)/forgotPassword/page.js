import Button from '../components/button';
import CheckoutInputField from '../components/checkoutInput';
import Title from '../components/title';

function ForgotPassword() {
  return (
    <div className="container pb-5  d-flex flex-column">
      <Title>Forgot Password</Title>
      <CheckoutInputField label={'Enter your Email'} />
      <Button classNameProp="w-100">Send Email</Button>
    </div>
  );
}

export default ForgotPassword;
