import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import ProductPage from '@/app/(customer)/product/page';

describe('ProductPage Component', () => {
  it('renders the product title', () => {
    const { container } = render(<ProductPage />);
    expect(container).toMatchSnapshot();
  });

  it('renders the add to cart button', () => {
    const { container } = render(<ProductPage />);
    expect(container).toMatchSnapshot();
  });
});