import '@testing-library/jest-dom';
import { render,screen } from '@testing-library/react';
import CartPage from '@/app/(customer)/cart/page';

describe('CartPage Component', () => {
  it('renders the cart title', () => {
    const { container } = render(<CartPage />);
    expect(container).toMatchSnapshot();
  });

  it('renders the checkout button', () => {
    const { container } = render(<CartPage />);
    expect(container).toMatchSnapshot();
  });
});