import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import CheckoutPage from '@/app/(customer)/checkout/page';

describe('CheckoutPage Component', () => {
  it('renders the checkout title', () => {
    const { container } = render(<CheckoutPage />);
    expect(container).toMatchSnapshot();
  });

  it('renders the payment section', () => {
    const { container } = render(<CheckoutPage />);
    expect(container).toMatchSnapshot();
  });
});