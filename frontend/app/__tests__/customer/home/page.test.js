import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import HomePage from '@/app/(customer)/home/page';

describe('HomePage Component', () => {
  it('renders the welcome message', () => {
    const { container } = render(<HomePage />);
    expect(container).toMatchSnapshot();
  });

  it('renders the featured products section', () => {
    const { container } = render(<HomePage />);
    expect(container).toMatchSnapshot();
  });
});